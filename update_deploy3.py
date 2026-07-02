import re
with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

old_block = """    - name: Decode Keystore
      env:
        KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
      run: |
        if [ -n "$KEYSTORE_BASE64" ]; then
          echo "$KEYSTORE_BASE64" | tr -d '' | base64 -d > my-upload-key.jks
        else
          echo "KEYSTORE_BASE64 is empty, using checked-in b64.txt"
          cat b64.txt | tr -d '' | base64 -d > my-upload-key.jks
        fi"""

new_block = """    - name: Decode Keystore
      env:
        KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
      run: |
        if [ -n "$KEYSTORE_BASE64" ]; then
          echo "$KEYSTORE_BASE64" | tr -d '\\n\\r' | base64 -d > my-upload-key.jks
        else
          echo "KEYSTORE_BASE64 is empty, using checked-in b64.txt"
          cat b64.txt | tr -d '\\n\\r' | base64 -d > my-upload-key.jks
        fi"""

content = content.replace(old_block, new_block)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
