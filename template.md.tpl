```
{%- for section_name, section_items in sections.items() if section_items%}
{{ section_name|title }}:
    {%- for section_item in section_items %}
- [{{ section_item.projects|join('/') }}] {{ section_item.action }}
    {%- endfor %}
{% endfor -%}
```
