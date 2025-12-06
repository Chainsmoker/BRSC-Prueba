import re

with open('temp.sql', 'r') as f:
    content = f.read()

# Buscar cualquier item que tenga el formato: 001-XXX-TA-002-23
fixed_content = re.sub(
    r"'(\d{3})-[A-Z]+-TA-(\d{3})-(\d{2})'",
    r"'TA-\1-\3'",
    content
)

with open('temp_fixed.sql', 'w') as f:
    f.write(fixed_content)

