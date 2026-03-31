import io
import zipfile 
import requests 
import frontmatter 
import json 
import os

# Create directories for persistence
os.makedirs('data/raw', exist_ok=True)

def read_repo_data(repo_owner, repo_name):
    """ Download and parse all markdown files from a GitHub repository

    Args: 
        repo_owner: Github username or organization 
        repo_name: Repository name

    Returns: 
        List of dictionaries containing file content and metadata
    """

    zip_path = f"data/raw/{repo_owner}_{repo_name}.zip"

    # --- STEP 1: CACHING LOGIC ---
    if os.path.exists(zip_path):
        print(f"Loading {repo_name} from local cache...")
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
    else:
        print(f"Downloading {repo_name} from GitHub...")
        prefix = 'https://codeload.github.com'
        url = f'{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main'
        resp = requests.get(url)

        if resp.status_code != 200:
            raise Exception(f"Failed to download repository: {resp.status_code}")
        
        zip_content = resp.content
        # Save to disk for next time
        with open(zip_path, 'wb') as f:
            f.write(zip_content)
    
    # --- STEP 2: PARSING LOGIC ---
    repository_data = []
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
        for file_info in zf.infolist(): 
            filename = file_info.filename 
            filename_lower = filename.lower() 

            if not (filename_lower.endswith(('.md', '.mdx', '.ipynb', '.rst'))):
                continue 
                    
            try: 
                with zf.open(file_info) as f_in:
                    content = f_in.read().decode('utf-8', errors='ignore')

                    if filename_lower.endswith('.ipynb'):
                        notebook = json.loads(content)
                        text_parts = [
                            ''.join(cell.get('source', [])) 
                            for cell in notebook.get('cells', []) 
                            if cell.get('source')
                        ]
                        data = {
                            'content': '\n\n'.join(text_parts), 
                            'metadata': {'filename': filename, 'type': 'notebook'}
                        }
                    else:
                        post = frontmatter.loads(content)
                        data = {
                            'content': post.content,
                            'metadata': {**post.metadata, 'filename': filename, 'type': 'text'}
                        }
                    repository_data.append(data)
            except Exception as e: 
                print(f"Error processing {filename}: {e}")
        
        return repository_data
    

# def read_repo_data(repo_owner, repo_name):
#     """ Download and parse all markdown files from a GitHub repository

#     Args: 
#         repo_owner: Github username or organization 
#         repo_name: Repository name

#     Returns: 
#         List of dictionaries containing file content and metadata
#     """

#     prefix = 'https://codeload.github.com'
#     url = f'{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main'
#     resp = requests.get(url)

#     if resp.status_code != 200:
#         raise Exception(f"Failed to download repository: {resp.status_code}")
    
#     repository_data = []
#     # zf = zipfile.ZipFile(io.BytesIO(resp.content))

#     with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
         
#         for file_info in zf.infolist(): 
#             filename = file_info.filename 
#             filename_lower = filename.lower() 

#             if not (filename_lower.endswith(('.md', '.mdx', '.ipynb', '.rst'))):
#                     continue 
                    
#             try: 
#                 with zf.open(file_info) as f_in:
#                     content = f_in.read().decode('utf-8', errors='ignore')

#                     ## 
#                     if filename_lower.endswith('.ipynb'):
                         
#                         notebook = json.loads(content)
#                         text_parts = []
#                         for cell in notebook.get('cells', []):
#                             source = ''.join(cell.get('source', []))
#                             if source.strip():
#                                 text_parts.append(source)
#                         data = {
#                             'content': '\n\n'.join(text_parts), 
#                             'filename': filename
#                         }
#                     else:
#                         ##
#                         post = frontmatter.loads(content)
#                         data = {
#                             'content': post.content, 
#                             'metadata': {**post.metadata, 'filename': filename}
#                         }
#                         data['filename'] = filename 

#                     repository_data.append(data)

#             except Exception as e: 
#                 print(f"Error processing {filename}: {e}")

#                 continue 
        
#         return repository_data
                 

# ## lets make a function call to use 
# # dtc_faq = read_repo_data('DataTalksClub', 'faq')
# # evidently_docs = read_repo_data('evidentlyai', 'docs')

# # print(f"FAQ documents: {len(dtc_faq)}")
# # print(f"Evidently documents: {len(evidently_docs)}")


# ## homework 
# sklearn_docs = read_repo_data('scikit-learn', 'scikit-learn');

# print(f"Scikit-learn documetns: {len(sklearn_docs)}")