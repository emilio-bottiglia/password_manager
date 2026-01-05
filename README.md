This Python-Tkinter password manager builds a GUI with spinboxes to parameterize entries for website, email, and password. 
create_password() samples uppercase, lowercase, digits, and symbols, shuffles the pool, then injects the generated secret into the password field.
Persistence is JSON based: a dict keyed by website serialized to credentials.json. save_credentials() loads or creates the file, merges new records, writes back, and clears widgets. 
find_password() looks up by website and surfaces the stored email and password via message boxes.
For stronger security, avoid plaintext JSON; persist secrets in environment variables, loading with os.environ, or use encrypted storage.
<img width="668" height="615" alt="image" src="https://github.com/user-attachments/assets/a1b967b5-f247-4b8b-8303-d84078e37d04" />

