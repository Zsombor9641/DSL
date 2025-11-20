# Social Media Content Planner DSL

A domain-specific language (DSL) for planning and configuring social media campaigns. This project provides a declarative syntax that enables marketing professionals to describe their campaigns in a structured way without requiring programming knowledge.

## Features

- **Declarative Syntax**: Easy-to-read, human-friendly language for defining campaigns
- **Multi-Platform Support**: Define content for Instagram, Facebook, Twitter, TikTok, LinkedIn, and YouTube
- **Content Scheduling**: Flexible scheduling options (daily, weekly, interval-based)
- **Audience Targeting**: Specify age ranges, interests, and locations
- **Budget Management**: Set total and daily budget limits with auto-optimization
- **Error Handling**: Comprehensive error detection and reporting

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd MyForm
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Requirements:

- Python 3.7+
- lark-parser >= 1.1.0
- pytest >= 7.0.0

## Quick Start

### Basic Example

Create a simple campaign file (e.g., `my_campaign.smp`):

```
campaign "basic_promo" duration(7 days) {
    platforms: [instagram, facebook]

    content_types {
        post "daily_update" {
            text: "Check out our latest products!"
            hashtags: ["#promo", "#sale"]
            schedule: daily at("12:00")
        }
    }
}
```

### Parse a Campaign

```python
from src.parser import SocialMediaContentParser

# Create parser instance
parser = SocialMediaContentParser()

# Parse a file
result = parser.parse_file('my_campaign.smp')

# Or parse a string directly
campaign_code = '''
campaign "test" duration(3 days) {
    platforms: [instagram]
    content_types {
        post "hello" {
            text: "Hello World!"
            schedule: daily at("10:00")
        }
    }
}
'''
result = parser.parse(campaign_code)
```

## Language Syntax

### Campaign Structure

```
campaign "<name>" duration(<time>) {
    platforms: [<platform_list>]

    content_types {
        <content_definitions>
    }

    targeting {
        <targeting_options>
    }

    budget {
        <budget_options>
    }
}
```

### Supported Platforms

- `instagram`
- `facebook`
- `twitter`
- `tiktok`
- `linkedin`
- `youtube`

### Content Types

- `post` - Regular social media post
- `story` - Story format (24-hour content)
- `reel` - Short-form video content
- `video` - Video content
- `image` - Image content

### Scheduling Options

```
// Daily scheduling
schedule: daily at("09:00", "15:00")

// Weekly scheduling
schedule: weekly on("Monday") at("10:00")

// Interval-based scheduling
schedule: every(2 hours) at("09:00") until("17:00")

// Specific time
schedule: at("12:00")
```

### Targeting

```
targeting {
    age_range: 18 to 45
    interests: ["technology", "gaming", "music"]
    location: ["New York", "Los Angeles"] optional
}
```

### Budget Management

```
budget {
    total: $1000
    daily_limit: $50 optional
    auto_optimize: true
}
```

## Project Structure

```
MyForm/
├── README.md                  # This file
├── documentation.md           # Detailed language specification
├── requirements.txt           # Python dependencies
├── src/
│   ├── __init__.py
│   ├── grammar.lark          # Lark grammar definition
│   └── parser.py             # Parser implementation
├── examples/
│   ├── basic_campaign.smp    # Simple campaign example
│   ├── complex_campaign.smp  # Advanced features example
│   └── error_examples.smp    # Error handling examples
└── tests/
    ├── test_parser.py        # Parser unit tests
    ├── test_error_handling.py # Error handling tests
    └── demo_tests.py         # Demo/integration tests
```

## Running Tests

Run all tests:

```bash
pytest tests/
```

Run specific test file:

```bash
pytest tests/test_parser.py
```

Run with verbose output:

```bash
pytest -v tests/
```

## Examples

### Simple Campaign

```
campaign "summer_sale" duration(14 days) {
    platforms: [instagram, facebook]

    content_types {
        post "sale_announcement" {
            text: "Summer sale is here! 50% off!"
            hashtags: ["#summersale", "#discount"]
            schedule: daily at("10:00")
        }
    }
}
```

### Advanced Campaign with Targeting and Budget

```
campaign "product_launch" duration(30 days) {
    platforms: [instagram, facebook, twitter]

    content_types {
        post "announcement" {
            text: "Introducing our new product!"
            media: "product_image.jpg"
            hashtags: ["#newproduct", "#innovation"]
            schedule: daily at("09:00", "15:00")
        }

        story "behind_scenes" {
            text: "See how we made it!"
            media: "bts_video.mp4"
            schedule: every(3 days) at("12:00")
        }
    }

    targeting {
        age_range: 25 to 54
        interests: ["technology", "innovation"]
        location: ["United States", "Canada"]
    }

    budget {
        total: $5000
        daily_limit: $200
        auto_optimize: true
    }
}
```

## Error Handling

The parser provides detailed error messages for:

- Syntax errors (missing brackets, invalid keywords)
- Lexical errors (invalid tokens)
- Semantic errors (invalid values, missing required fields)

Example error output:

```
Syntax Error at line 3, column 15:
Expected ']' but found ','
    platforms: [instagram, facebook,]
                                    ^
```

## Documentation

For detailed language specification, syntax rules, and semantic definitions, see:

- [documentation.md](documentation.md) - Complete language specification

## Development

### Adding New Features

1. Update the grammar in `src/grammar.lark`
2. Add corresponding transformer methods in `src/parser.py`
3. Add tests in `tests/`
4. Update documentation

### Grammar Development

The grammar is defined using [Lark](https://lark-parser.readthedocs.io/), a modern parsing toolkit for Python. The grammar file (`src/grammar.lark`) uses EBNF-like syntax.

## License

This project is for educational purposes as part of a formal languages course.

## Contributing

This is an academic project. For suggestions or bug reports, please contact the project maintainer.

## Author

Created as part of the Formal Languages course at university.
