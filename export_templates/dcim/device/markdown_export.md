|Hostname|Status|Location|
|:--|:--|:--|
{% for device in queryset -%}
|{{ device.name }}|{{ device.status }}|{{ device.location }}|
{% endfor %}
