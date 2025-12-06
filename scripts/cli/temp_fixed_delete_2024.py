import re

with open('temp.sql', 'r') as f:
    lines = f.readlines()

fixed_lines = []

for line in lines:
    # Transformar el item
    line = re.sub(
        r"'(\d{3})-[A-Z]+-TA-(\d{3})-(\d{2})'",
        r"'TA-\1-\3'",
        line
    )
    
    # Después de transformar, revisamos si termina en -24
    match = re.search(r"'TA-\d{3}-24'", line)
    
    if not match:
        fixed_lines.append(line)

with open('temp_fixed.sql', 'w') as f:
    f.writelines(fixed_lines)
