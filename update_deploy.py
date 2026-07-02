import re
with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

old_block = """    - name: Decode Keystore
      run: |
        echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > my-upload-key.jks"""

new_block = """    - name: Decode Keystore
      env:
        KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
      run: |
        if [ -n "$KEYSTORE_BASE64" ]; then
          echo "$KEYSTORE_BASE64" | base64 -d > my-upload-key.jks
        else
          echo "KEYSTORE_BASE64 is empty, using checked-in my-upload-key.jks"
        fi"""

content = content.replace(old_block, new_block)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
