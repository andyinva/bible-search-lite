cd ~/projects/bible-search-lite/database
# Create the compressed version for distribution
python3 -c "
import zipfile
import os

with zipfile.ZipFile('bible_data.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('bibles.db', 'bibles.db')
    print(f'Created bible_data.zip: {os.path.getsize(\"bible_data.zip\") / 1024 / 1024:.1f} MB')
"