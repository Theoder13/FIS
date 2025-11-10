import requests
import base64
import os

def read_file_from_github(repo_owner, repo_name, file_path, branch="main", github_token="some_token"):
    """
    Read a file from a GitHub repository.
    
    Args:
        repo_owner: GitHub username or organization
        repo_name: Repository name
        file_path: Path to file in the repository
        branch: Branch name (default: main)
        github_token: GitHub personal access token (optional for public repos)
    
    Returns:
        File content as bytes or string
    """
    # Construct the API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    # Set up headers
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Add authentication if token is provided
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    # Set up parameters
    params = {
        "ref": branch
    }
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse the response
        data = response.json()
        
        # Decode the content (GitHub returns base64 encoded content)
        content = base64.b64decode(data['content'])
        
        return content
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: File not found at path '{file_path}'")
        elif response.status_code == 401:
            print("Error: Authentication failed. Check your token.")
        else:
            print(f"HTTP Error: {e}")
        raise
    except Exception as e:
        print(f"Error reading file from GitHub: {e}")
        raise


def save_file_locally(content, local_path):
    """Save the downloaded content to a local file."""
    with open(local_path, 'wb') as f:
        f.write(content)
    print(f"File saved to: {local_path}")


# Main execution
if __name__ == "__main__":
    # Configuration - STORE TOKEN IN ENVIRONMENT VARIABLE
    repo_owner = "Theoder13"
    repo_name = "aava"
    branch = "main"
    file_path = "python/Document 1.pdf"  # Updated to include the full path
    
    # IMPORTANT: Use environment variable for token
    github_token = os.getenv(Token)  # Get from environment
    
    # If you must hardcode temporarily for testing (NOT RECOMMENDED):
    # github_token = "your_new_token_here"
    
    if not github_token:
        print("Warning: No GitHub token provided. This only works for public repositories.")
    
    try:
        # Read the file
        print(f"Reading file from GitHub: {file_path}")
        content = read_file_from_github(
            repo_owner=repo_owner,
            repo_name=repo_name,
            file_path=file_path,
            branch=branch,
            github_token=github_token
        )
        
        # Save locally
        local_filename = "Document 1.pdf"
        save_file_locally(content, local_filename)
        
        print(f"Successfully downloaded {len(content)} bytes")
        
    except Exception as e:
        print(f"Failed to download file: {e}")