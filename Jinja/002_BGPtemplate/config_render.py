import yaml
from jinja2 import Template
from argparse import ArgumentParser

parser = ArgumentParser("Specifying the YAML File")

parser.add_argument("-d", "--data-file",
                    help="Please specify the YAMl file.",
                    required=True
                   )
parser.add_argument("-t", "--template-file",
                    help="Please specify the Jinja template file.",
                    required=True
                   )
args = parser.parse_args()

# data_file_name = "routerBGP-Data.yaml"
# template_file_name = "bgp_Template.j2"
data_file_name = args.data_file
template_file_name = args.template_file

# Verifies whether the provided data and template file exist before continuing
try:
  with open(data_file_name) as f:
      yaml_data = yaml.safe_load(f)

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

except FileNotFoundError as e:
  print(e)
