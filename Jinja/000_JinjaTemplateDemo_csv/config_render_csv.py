import csv
from jinja2 import Template

source_file = "Switch-Interface_csv.csv"
template_file = "Switch_Template_csv.j2"
configuration_file = "Switch_Configuration_csv.txt"

# Stores the entire configuration generated by Jinja
switch_configs = ""

with open(template_file) as f:
  interface_template = Template(f.read(), keep_trailing_newline=True)

with open(source_file) as f:
  reader = csv.DictReader(f)
  for row in reader:
    interface_config = interface_template.render(
      interface = row["interface"],
      vlan = row["vlan"],
      server = row["server"],
      link = row["link"],
      purpose = row["purpose"]
    )
    switch_configs += interface_config

print(switch_configs)

with open(configuration_file, "w") as f:
  f.write(switch_configs)
