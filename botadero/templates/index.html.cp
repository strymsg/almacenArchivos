<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
	<head>
		 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		 <link rel="shortcut icon" href="../static/botadero_resources/favicon.png">
		<title>Archivador temporal para compartir archivos</title>
		<link rel="stylesheet" href="../static/{{ esquema_colores }}/base.css" type="text/css" />

	</head>
	<body>

	<h1><a href="/">"El botadero"</a></h1>
		<div class="qu">
			Un sitio <b>público</b> para compartir archivos	
		</div>

	<!-- Categorias -->	
	<div id="categorias">
	  {% for cat_na in categorias_con_nums %}
		{% if cat_na[0] == categoria_actual %}
		  {% if cat_na[0] == "" %} <!-- Dummy -->
	            <span class="categoria"><a href="/" > #Misc.</a>({{ cat_na[1] }})</span>
		  {% else %}
  		    <span class="categoria"><a href="/{{ categoria_actual }}/" > #{{ categoria_actual }}</a>({{ cat_na[1] }})</span>
		  {% endif %}			
		{% else %}
		    {% if cat_na[0] == "" %} <!-- Dummy -->
	               <a href="/" > #Misc.</a>({{ cat_na[1] }})</span>
		    {% else %}
  		       <a href="/{{ cat_na[0] }}/" > #{{ cat_na[0] }}</a>({{ cat_na[1] }})</span>
		    {% endif %}			
		{% endif%}
	  {% endfor %}
	</div>

		
	<div class="container">
	<!-- Subida de archivos -->		
	<div class="nota"> 
	{% if categoria_actual == "" %}
		<form method="post" id="upload_file" action="/almacen/upload_file" enctype="multipart/form-data">
	{% else %}
		<form method="post" id="upload_file" action="/almacen/{{ categoria_actual }}/upload_file" enctype="multipart/form-data">	
	{% endif %}
			<input type="file" name="file"/>
			<input type="submit", class="btn", value="Compartir archivo"/>
				<p>Los archivos se eliminan después de {{ borrar_1 }} a {{ borrar_2 }} días, dependiendo su tamaño.
					 <a href="/info" >ver información</a>
				 </p>
		</form>	
	</div>	

	<!-- Estadisticas generales -->
	{{ esp_disp }} MB disponibles (<b>{{ p_disp }} %</b>) Total de <b>{{ num_arch }}</b> archivos
	

	<!-- Listado de Archivos -->	
		
	
	<table 	<div class="class="table">
		<tr>
			<th>Archivos compartidos en <i>{{ categoria_actual }}</i></th>	
			<th>TAMAÑO</th>
			<th>Días para borrado</th>
		</tr>
		{% for reg_arch in lista_archivos|reverse %}
		<tr>
			<td>
			{% if categoria_actual != "" %}
				<a href="/{{ reg_arch[0] }}/{{ categoria_actual }}/{{ reg_arch[1] }}">
				{# Agregado para partir archivos con nombre grande #}				
					{% for c in reg_arch[1] %}{% if loop.index % 37 == 0 %}<br>{% endif %}{{ c }}{% endfor %}
				</a>
			{% else %}
				<a href="/{{ reg_arch[0] }}/{{ reg_arch[1] }}">
				{# Agregado para partir archivos con nombre grande #}				
					{% for c in reg_arch[1] %}{% if loop.index % 37 == 0 %}<br>{% endif %}{{ c }}{% endfor %}
				</a>
			{% endif %}		
			</td>
			
			<td > {{ reg_arch[2] }} </td>
			<td class="dias_restantes">
			{% if reg_arch[3]|int >= 10 %}
				<span id="dias_muchos" > {{ reg_arch[3] }} </span>
			{% elif reg_arch[3]|int < 10 and reg_arch[3]|int > 3 %}
				<span id="dias_moderados" > {{ reg_arch[3] }} </span>
			{% elif reg_arch[3]|int <= 3 %}
				<span id="dias_pocos" > {{ reg_arch[3] }} </span>
			{% endif %}
			</td>
		</tr>
		{% endfor %}

	</table>
	</div>
	<!-- Categorias -->	
	<div id="categorias">
	  {% for cat_na in categorias_con_nums %}
		{% if cat_na[0] == categoria_actual %}
		  {% if cat_na[0] == "" %} <!-- Dummy -->
	            <span class="categoria"><a href="/" > #Misc.</a>({{ cat_na[1] }})</span>
		  {% else %}
  		    <span class="categoria"><a href="/{{ categoria_actual }}/" > #{{ categoria_actual }}</a>({{ cat_na[1] }})</span>
		  {% endif %}			
		{% else %}
		    {% if cat_na[0] == "" %} <!-- Dummy -->
	               <a href="/" > #Misc.</a>({{ cat_na[1] }})</span>
		    {% else %}
  		       <a href="/{{ cat_na[0] }}/" > #{{ cat_na[0] }}</a>({{ cat_na[1] }})</span>
		    {% endif %}			
		{% endif%}
	  {% endfor %}
	</div>

	<!-- Notas al pie -->
	<div class="nota">
	<p>Revisa las <a href="/estadisticas" > estadisticas </a> de los archivos.
	</p>
	</div>
	
	<!-- Notas al pie -->
	<div class="qu">
		<p>Compartir es bueno</p>
		<p> <a href="https://notabug.org/r00thouse/botadero">Código fuente</a> de esta aplicación.  </p>
	</div>
	</body>

</html>
