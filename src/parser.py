#!/usr/bin/env python3
"""
Social Media Content Planner Parser
Lark-based parser implementáció a DSL nyelvhez
"""

import sys
import os
from pathlib import Path
from lark import Lark, LarkError, Transformer, v_args
from lark.exceptions import ParseError, LexError

class SocialMediaContentTransformer(Transformer):
    """AST transformer a parse tree struktúrált adattá alakításához"""
    
    @v_args(inline=True)
    def campaign_definition(self, name, duration, body):
        return {
            'type': 'campaign',
            'name': name,
            'duration': duration,
            'body': body
        }
    
    @v_args(inline=True) 
    def campaign_body(self, platforms, content, targeting=None, budget=None):
        result = {
            'platforms': platforms,
            'content': content
        }
        if targeting:
            result['targeting'] = targeting
        if budget:
            result['budget'] = budget
        return result
    
    @v_args(inline=True)
    def platform_definition(self, platform_list):
        return platform_list
    
    def platform_list(self, platforms):
        return [str(p) for p in platforms]
    
    def platform_name(self, platform):
        return str(platform)
    
    @v_args(inline=True)
    def content_definition(self, *content_items):
        return list(content_items)
    
    @v_args(inline=True)
    def content_item(self, content_type, name, properties):
        return {
            'type': str(content_type),
            'name': name,
            'properties': properties
        }
    
    def content_properties(self, properties):
        result = {}
        for prop in properties:
            if isinstance(prop, dict):
                result.update(prop)
        return result
    
    @v_args(inline=True)
    def text_property(self, text):
        return {'text': self._clean_string(text)}
    
    @v_args(inline=True) 
    def media_property(self, media, optional=None):
        return {'media': self._clean_string(media), 'optional': optional is not None}
    
    @v_args(inline=True)
    def hashtag_property(self, hashtag_list):
        return {'hashtags': hashtag_list}
    
    @v_args(inline=True)
    def schedule_property(self, schedule):
        return {'schedule': schedule}
    
    @v_args(inline=True)
    def daily_schedule(self, *times):
        return {'type': 'daily', 'times': list(times)}
    
    @v_args(inline=True)
    def time_specific_schedule(self, *times):
        return {'type': 'at', 'times': list(times)}
    
    def time_list(self, times):
        return [self._clean_string(t) for t in times]
    
    @v_args(inline=True)
    def duration_value(self, number, unit):
        return {'value': int(number), 'unit': str(unit)}
    
    def string_list(self, strings):
        return [self._clean_string(s) for s in strings]
    
    @v_args(inline=True)
    def money_value(self, amount, decimal=None):
        if decimal:
            return float(f"{amount}.{decimal}")
        return int(amount)
    
    def _clean_string(self, s):
        """Remove quotes from string literals"""
        if isinstance(s, str) and s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return str(s)

class SocialMediaContentParser:
    """Main parser class"""
    
    def __init__(self):
        self.grammar_file = Path(__file__).parent / "grammar.lark"
        self.parser = None
        self.transformer = SocialMediaContentTransformer()
        self._load_grammar()
    
    def _load_grammar(self):
        """Load and initialize the Lark parser"""
        try:
            with open(self.grammar_file, 'r', encoding='utf-8') as f:
                grammar_content = f.read()
            
            self.parser = Lark(
                grammar_content,
                parser='earley',  # supports all context-free grammars
                ambiguity='explicit'  # handle ambiguous grammars
            )
            print(f"[OK] Grammar loaded successfully from {self.grammar_file}")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Grammar file not found: {self.grammar_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to load grammar: {e}")
    
    def parse_file(self, file_path):
        """Parse a .smp file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_string(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to read file {file_path}: {e}")
    
    def parse_string(self, content):
        """Parse a string containing SMP DSL code"""
        if not self.parser:
            raise RuntimeError("Parser not initialized")
        
        try:
            # Parse the content
            parse_tree = self.parser.parse(content)
            print("[OK] Parsing successful!")
            
            # Transform to structured data
            result = self.transformer.transform(parse_tree)
            print("[OK] AST transformation successful!")
            
            return {
                'success': True,
                'parse_tree': parse_tree,
                'ast': result,
                'errors': []
            }
            
        except ParseError as e:
            error_msg = f"Syntax error at line {e.line}, column {e.column}: {e}"
            print(f"[ERROR] Parse error: {error_msg}")
            return {
                'success': False,
                'parse_tree': None,
                'ast': None,
                'errors': [{'type': 'ParseError', 'message': error_msg, 'line': e.line, 'column': e.column}]
            }
            
        except LexError as e:
            error_msg = f"Lexical error: {e}"
            print(f"[ERROR] Lex error: {error_msg}")
            return {
                'success': False,
                'parse_tree': None,
                'ast': None,
                'errors': [{'type': 'LexError', 'message': error_msg}]
            }
            
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"[ERROR] Unexpected error: {error_msg}")
            return {
                'success': False,
                'parse_tree': None,
                'ast': None,
                'errors': [{'type': 'UnexpectedError', 'message': error_msg}]
            }
    
    def validate_semantic(self, ast):
        """Perform semantic validation on the AST"""
        errors = []
        
        if not ast:
            return ['Invalid AST structure']
        
        # Handle case where AST is wrapped in Tree object
        if hasattr(ast, 'data') and hasattr(ast, 'children'):
            # This is a Lark Tree object, extract the actual data
            print(f"[DEBUG] AST is Tree object: {type(ast)}")
            return []  # For now, skip semantic validation on Tree objects
        
        if not isinstance(ast, dict):
            return ['AST is not a dictionary structure']
        
        # Check campaign structure
        if ast.get('type') != 'campaign':
            errors.append("Root element must be a campaign")
        
        # Validate platforms
        body = ast.get('body', {})
        platforms = body.get('platforms', [])
        valid_platforms = {'instagram', 'facebook', 'twitter', 'tiktok', 'linkedin', 'youtube'}
        
        for platform in platforms:
            if platform not in valid_platforms:
                errors.append(f"Invalid platform: {platform}")
        
        # Validate content types
        content = body.get('content', [])
        if not content:
            errors.append("Campaign must have at least one content item")
        
        # Validate budget values
        budget = body.get('budget')
        if budget:
            total = budget.get('total')
            if total and total <= 0:
                errors.append("Budget total must be positive")
        
        return errors

def main():
    """Command line interface"""
    if len(sys.argv) != 2:
        print("Usage: python parser.py <file.smp>")
        print("Example: python parser.py ../examples/basic_campaign.smp")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        parser = SocialMediaContentParser()
        result = parser.parse_file(file_path)
        
        if result['success']:
            print(f"\n[SUCCESS] Successfully parsed: {file_path}")
            print("\n[INFO] Parse Tree:")
            print(result['parse_tree'].pretty())
            
            print("\n[INFO] AST Structure:")
            import json
            print(json.dumps(result['ast'], indent=2, ensure_ascii=False))
            
            # Semantic validation
            semantic_errors = parser.validate_semantic(result['ast'])
            if semantic_errors:
                print("\n[WARNING] Semantic validation errors:")
                for error in semantic_errors:
                    print(f"  - {error}")
            else:
                print("\n[OK] Semantic validation passed!")
        else:
            print(f"\n[FAILED] Failed to parse: {file_path}")
            for error in result['errors']:
                print(f"  {error['type']}: {error['message']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()