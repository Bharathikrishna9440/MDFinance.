import re
with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = re.sub(r'    - name: Decode Keystore.*?    - name: Get Version Info',
"""    - name: Decode Keystore
      env:
        KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
      run: |
        if [ -n "$KEYSTORE_BASE64" ]; then
          echo "$KEYSTORE_BASE64" | base64 --decode --ignore-garbage > my-upload-key.jks
        else
          echo "KEYSTORE_BASE64 is empty, using checked-in b64.txt"
          grep -v "==>" b64.txt | base64 --decode --ignore-garbage > my-upload-key.jks
        fi

    - name: Get Version Info""", content, flags=re.DOTALL)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
