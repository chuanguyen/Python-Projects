import yaml
from jinja2 import Template

data_file_name = "routerBGP-Data.yaml"
template_file_name = "bgp_Template.j2"

with open(data_file_name) as f:
    yaml_data = yaml.load(f)

with open(template_file_name) as f:
    template_file = Template(f.read(), keep_trailing_newline=True)

for node in yaml_data:

  # Stores full configuration that will be exported to a file
  generated_configs = template_file.render(rid=node['rid'],
                                          local_asn=node['local_asn'],
                                          neighbors=node['neighbors'],
                                          networks=node['networks']
                                         )

  with open("{}_BGP-config.txt".format(node['hostname']), "w") as f:
    f.write(generated_configs)
