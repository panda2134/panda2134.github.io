---
layout: default
title: Panda_2134's Blog
---

# Recent Blogs
---
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}"><h2>{{ post.title }}</h2> </a>
      {{post.excerpt}}
    </li>
  {% endfor %}
</ul>>
