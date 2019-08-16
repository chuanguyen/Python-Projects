import yaml
from jinja2 import Template

data_file_name = "device-data.yaml"
template_file_name = "Switch_Template.j2"

# Stores full configuration that will be exported to a file
generated_configs = ""

with open(data_file_name) as f:
    yaml_data = yaml.load(f)

with open(template_file_name) as f:
    template_file = Template(f.read(), keep_trailing_newline=True)

for node in yaml_data:
  for interface in node["interfaces"]:
    config = template_file.render(name=interface['name'],
                                  server=interface['server'],
                                  link=interface['link'],
                                  purpose=interface['purpose'],
                                  vlan=interface['vlan']
                                  )
    generated_configs += config

  with open("{}_config.txt".format(node['hostname']), "w") as f:
    f.write(generated_configs)
