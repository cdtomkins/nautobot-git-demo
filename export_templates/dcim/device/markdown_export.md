|Hostname|Status|Site|
|:--|:--|:--|
{% for device in queryset -%}
|{{ device.name }}|{{ device.status }}|{{ device.site }}|
{% endfor %}
