# Ansible Collection - polaris.deploy

Documentation for the collection.

# tomcat_jndi_resources and tomcat_jndi_resource_link

if "using_alt_app_dir" is provided the "tomcat_server.xml.j2" file will add a context attribute to the server.xml file. Further more we are allowing one or more local resource link to be added which allows the GlobalNamingResources to be available to the deployed application.
