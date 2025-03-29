
python3 src/main.py "/Static_Site_Gen/"


#Fix links by appending /index.html
find docs/ -type f -name "*.html" -exec sed -i 's/href="\(\/Static_Site_Gen\/[^"]*\)"/href="\1\/index.html"/g' {} +