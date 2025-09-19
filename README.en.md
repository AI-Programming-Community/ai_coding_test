# AI Coding Test Questions Repository

## Project Introduction

This is a dedicated repository of test questions for evaluating AI coding capabilities. It includes test cases across various programming languages and scenarios to assess and verify AI performance in code generation, debugging, optimization, and more.

## Project Structure

```
.
├── README.md          # Chinese documentation
├── README.en.md       # English documentation  
├── LICENSE            # License file
└── questions/         # Test questions directory
```

## Usage

1. Clone this repository
2. Select the appropriate question directory as needed
3. Review the problem description and requirements
4. Write or modify code to solve the problem
5. Open the HTML file in a browser to verify results

## Current Test Questions

### HTML/CSS Navigation Layout Problem
- **Location**: `questions/html-css-navigation/`
- **Problem**: Navigation bar is currently left-aligned, needs to be centered
- **Files**: 
  - `index.html` - HTML file with navigation structure
  - `styles.css` - CSS styles file that needs modification
- **Hint**: Check the comments in the CSS file to find the property that needs to be changed

### Left-side Navigation Interaction Problem
- **Location**: `questions/left-side-navigation/`
- **Problem**: Left-side navigation needs to be hidden by default and slide out when mouse moves to the left edge
- **Files**: 
  - `index.html` - HTML file with left-side navigation structure
  - `styles.css` - CSS styles file that needs modification
- **Hint**: Need to add hover effects and slide animations

### Redis Concurrent Reading Cache Problem
- **Location**: `questions/concurrent-redis-reading/`
- **Problem**: Redis caching service has concurrent reading bugs that need to be discovered and fixed by running test_cache.py
- **Files**: 
  - `app.py` - Flask application main file
  - `test_cache.py` - Test file for discovering bugs
  - `requirements.txt` - Python dependencies file
- **Hint**: Run the test file to discover specific issues, fix bugs related to concurrent reading

### HTML to Markdown Table Support
- **Location**: `questions/html-to-markdown/`
- **Problem**: Existing Ruby function cannot properly handle HTML table conversion to Markdown
- **Files**: 
  - `html_to_markdown.rb` - Ruby conversion function file
  - `readme.md` - Problem description file
- **Hint**: Need to add table conversion functionality, supporting HTML table to Markdown table conversion

### Log Analyzer
- **Location**: `log-analyzer`
- **Problem Description**: Write a program to read a very large log file (e.g., hundreds of MB of text)
  - Format: `[2025-09-19 12:30:45] INFO user_name action_name job_status`
  - Requirements: Count the number of operations per user, count the occurrences of each Action
  - Output: A JSON formatted report including user statistics, Action statistics, and ERROR ratio
  - The program must support streaming read (cannot load the entire file into memory at once).

### Multi-threaded Web Crawler
- **Problem Description**: Implement a simple concurrent web crawler
  - Input a starting URL and depth n
  - Recursively crawl links on the page until depth n is reached
  - Use multi-threading/coroutines to accelerate requests
  - Count the total number of pages visited and the number of pages containing specified keywords
  - If encountering non-HTML pages such as docx, pdf, etc., ensure the filenames are saved correctly
  - All downloaded static pages should be able to link to each other for navigation

## Contributing

Contributions of new test cases and improvements are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.