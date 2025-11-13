# TRANSFORM THE REPORTED DATA

## Remove unnecessary lines
# - 0 product pages
# - duplicated .../pages/X links

# [340 products] https://venbo.shop/cat-producto/libros/libros-formatos/libros-papel
# [91 products] https://venbo.shop/cat-producto/moda/moda-ninos
# [85 products] https://venbo.shop/cat-producto/electronica/electronica-balanzas
# [55 products] https://venbo.shop/cat-producto/alimentacion/conservas
# [51 products] https://venbo.shop/cat-producto/moda/moda-bebe
# [45 products] https://venbo.shop/cat-producto/alimentacion/sin-gluten
# [44 products] https://venbo.shop/cat-producto/libros/libros-formatos/libros-electronicos
# [41 products] https://venbo.shop/cat-producto/electronica/electronica-domotica
# [39 products] https://venbo.shop/cat-producto/alimentacion/comida-vegana
# [37 products] https://venbo.shop/cat-producto/suministros-industriales/suministrosindustriales-limpieza
# [36 products] https://venbo.shop/cat-producto/alimentacion/comida-vegetariana
# [34 products] https://venbo.shop/cat-producto/papeleria/papeleria-escritura
# [34 products] https://venbo.shop/cat-producto/alimentacion/chocolates-dulces
# [33 products] https://venbo.shop/cat-producto/suministros-industriales/productos-quimicos
# [27 products] https://venbo.shop/cat-producto/artesania/artesania-textil
# [22 products] https://venbo.shop/cat-producto/juguetes/juguetes-bebes
# [15 products] https://venbo.shop/cat-producto/informatica-oficina/hardware
# [15 products] https://venbo.shop/cat-producto/alimentacion/pastas-y-harinas
# [15 products] https://venbo.shop/cat-producto/electronica/electronica-iluminacion
# [14 products] https://venbo.shop/cat-producto/reservas/reservas-hoteles
# [14 products] https://venbo.shop/cat-producto/electronica/electronica-videovigilancia
# [13 products] https://venbo.shop/cat-producto/moda/moda-adolescentes
# [11 products] https://venbo.shop/cat-producto/artesania/artesania-madera
# [8 products] https://venbo.shop/cat-producto/artesania/artesania-ceramica
# [8 products] https://venbo.shop/cat-producto/informatica-oficina/informatica-laptops
# [6 products] https://venbo.shop/cat-producto/alimentacion/sin-lactosa
# [6 products] https://venbo.shop/cat-producto/salud/test-y-medicion
# [5 products] https://venbo.shop/cat-producto/electronica/electronica-enchufes
# [5 products] https://venbo.shop/cat-producto/electronica/televisores
# [5 products] https://venbo.shop/cat-producto/alimentacion/cereales-frutos-secos-y-semillas
# [5 products] https://venbo.shop/cat-producto/bioseguridad/bioseguridad-barbijos
# [4 products] https://venbo.shop/cat-producto/juguetes/juguetes-mesacartas
# [4 products] https://venbo.shop/cat-producto/electronica/electronica-asistentes
# [4 products] https://venbo.shop/cat-producto/artesania/artesania-chala
# [4 products] https://venbo.shop/cat-producto/bebidas/cafe-te-refrescos
# [4 products] https://venbo.shop/cat-producto/juguetes/juguetes-construccionespuzzles
# [4 products] https://venbo.shop/cat-producto/alimentacion/aperitivos
# [3 products] https://venbo.shop/cat-producto/papeleria/pinturas
# [3 products] https://venbo.shop/cat-producto/suministros-industriales/suministrosindustriales-herramientasutensilios
# [3 products] https://venbo.shop/cat-producto/informatica-oficina/insumos
# [3 products] https://venbo.shop/cat-producto/informatica-oficina/software
# [3 products] https://venbo.shop/cat-producto/papeleria/utiles-escolares
# [2 products] https://venbo.shop/cat-producto/alimentacion/salsas-aderezos
# [2 products] https://venbo.shop/cat-producto/servicios-profesionales/servicios-legales
# [2 products] https://venbo.shop/cat-producto/vending/vending-suministros
# [2 products] https://venbo.shop/cat-producto/suministros-industriales/suministrosindustriales-agricultura
# [2 products] https://venbo.shop/cat-producto/vending/vending-mecanic
# [43 products] https://venbo.shop/cat-producto/alimentacion/lacteos/quesos
# [31 products] https://venbo.shop/cat-producto/libros/comics/comics-dc
# [29 products] https://venbo.shop/cat-producto/hogar/cocina
# [27 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-saludrespiratoria
# [27 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-peliculas
# [24 products] https://venbo.shop/cat-producto/libros/comics/comics-manga
# [24 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-cuidadopersonal
# [20 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-aliviodolor
# [20 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-dermatologia
# [18 products] https://venbo.shop/cat-producto/hogar/hogar-decoracion
# [13 products] https://venbo.shop/cat-producto/moda/moda-calzado/calzado-deportivo
# [12 products] https://venbo.shop/cat-producto/cine-musica-fotos/fotografia/fotografia-paisajes
# [12 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-saluddigestiva
# [12 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-primerosauxilios
# [11 products] https://venbo.shop/cat-producto/cine-musica-fotos/fotografia/fotografia-panoramicas
# [10 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-maternidad
# [10 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-vitaminas
# [9 products] https://venbo.shop/cat-producto/hogar/hogar-limpieza
# [3 products] https://venbo.shop/cat-producto/libros/comics/comics-disney
# [3 products] https://venbo.shop/cat-producto/libros/comics/comics-bolivianos
# [3 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-documentales
# [3 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/discografias
# [2 products] https://venbo.shop/cat-producto/moda/moda-calzado/moda-calzadobotas
# [2 products] https://venbo.shop/cat-producto/cine-musica-fotos/fotografia/fotografia-personas
# [2 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-antiparasitarios
# [2 products] https://venbo.shop/cat-producto/salud/medicamentos/medicamentos-cardiologi
# [101 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-formatos/mp3
# [29 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-ubicacion/videos-nacionales
# [28 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-formato/videos-dvd
# [27 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/folclore-oriental
# [26 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/folclore-vallegrandino
# [15 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-generos/drama
# [14 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/pop
# [12 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/rock
# [8 products] https://venbo.shop/cat-producto/hogar/mascotas-hogar/medicamentos-veterinaria
# [8 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/folclore
# [7 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-formatos/video
# [4 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/instrumental
# [3 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/metal
# [3 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/jazz
# [2 products] https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-formato/videos-streaming
# [2 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/blues
# [2 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/hip-hop
# [2 products] https://venbo.shop/cat-producto/cine-musica-fotos/musica/musica-estilos/funk


## Transform into a dictionary

categories = {
  '/libros/libros-formatos/libros-papel': 340,
  '/moda/moda-ninos': 91,
  '/electronica/electronica-balanzas': 85,
  '/alimentacion/conservas': 55,
  '/moda/moda-bebe': 51,
  '/alimentacion/sin-gluten': 45,
  '/libros/libros-formatos/libros-electronicos': 44,
  '/electronica/electronica-domotica': 41,
  '/alimentacion/comida-vegana': 39,
  '/suministros-industriales/suministrosindustriales-limpieza': 37,
  '/alimentacion/comida-vegetariana': 36,
  '/papeleria/papeleria-escritura': 34,
  '/alimentacion/chocolates-dulces': 34,
  '/suministros-industriales/productos-quimicos': 33,
  '/artesania/artesania-textil': 27,
  '/juguetes/juguetes-bebes': 22,
  '/informatica-oficina/hardware': 15,
  '/alimentacion/pastas-y-harinas': 15,
  '/electronica/electronica-iluminacion': 15,
  # '/reservas/reservas-hoteles': 14,
  '/electronica/electronica-videovigilancia': 14,
  '/moda/moda-adolescentes': 13,
  '/artesania/artesania-madera': 11,
  '/artesania/artesania-ceramica': 8,
  '/informatica-oficina/informatica-laptops': 8,
  '/alimentacion/sin-lactosa': 6,
  '/salud/test-y-medicion': 6,
  '/electronica/electronica-enchufes': 5,
  '/electronica/televisores': 5,
  '/alimentacion/cereales-frutos-secos-y-semillas': 5,
  '/bioseguridad/bioseguridad-barbijos': 5,
  '/juguetes/juguetes-mesacartas': 4,
  '/electronica/electronica-asistentes': 4,
  '/artesania/artesania-chala': 4,
  '/bebidas/cafe-te-refrescos': 4,
  '/juguetes/juguetes-construccionespuzzles': 4,
  '/alimentacion/aperitivos': 4,
  '/papeleria/pinturas': 3,
  '/suministros-industriales/suministrosindustriales-herramientasutensilios': 3,
  '/informatica-oficina/insumos': 3,
  '/informatica-oficina/software': 3,
  '/papeleria/utiles-escolares': 3,
  '/alimentacion/salsas-aderezos': 2,
  # '/servicios-profesionales/servicios-legales': 2,
  '/vending/vending-suministros': 2,
  '/suministros-industriales/suministrosindustriales-agricultura': 2,
  '/vending/vending-mecanic': 2,
  '/alimentacion/lacteos/quesos': 43,
  '/libros/comics/comics-dc': 31,
  '/hogar/cocina': 29,
  '/salud/medicamentos/medicamentos-saludrespiratoria': 27,
  '/cine-musica-fotos/videos/videos-peliculas': 27,
  '/libros/comics/comics-manga': 24,
  '/salud/medicamentos/medicamentos-cuidadopersonal': 24,
  '/salud/medicamentos/medicamentos-aliviodolor': 20,
  '/salud/medicamentos/medicamentos-dermatologia': 20,
  '/hogar/hogar-decoracion': 18,
  '/moda/moda-calzado/calzado-deportivo': 13,
  '/cine-musica-fotos/fotografia/fotografia-paisajes': 12,
  '/salud/medicamentos/medicamentos-saluddigestiva': 12,
  '/salud/medicamentos/medicamentos-primerosauxilios': 12,
  '/cine-musica-fotos/fotografia/fotografia-panoramicas': 11,
  '/salud/medicamentos/medicamentos-maternidad': 10,
  '/salud/medicamentos/medicamentos-vitaminas': 10,
  '/hogar/hogar-limpieza': 9,
  '/libros/comics/comics-disney': 3,
  '/libros/comics/comics-bolivianos': 3,
  '/cine-musica-fotos/videos/videos-documentales': 3,
  '/cine-musica-fotos/musica/discografias': 3,
  '/moda/moda-calzado/moda-calzadobotas': 2,
  '/cine-musica-fotos/fotografia/fotografia-personas': 2,
  '/salud/medicamentos/medicamentos-antiparasitarios': 2,
  '/salud/medicamentos/medicamentos-cardiologi': 2,
  '/cine-musica-fotos/musica/musica-formatos/mp3': 101,
  '/cine-musica-fotos/videos/videos-ubicacion/videos-nacionales': 29,
  '/cine-musica-fotos/videos/videos-formato/videos-dvd': 28,
  '/cine-musica-fotos/musica/musica-estilos/folclore-oriental': 27,
  '/cine-musica-fotos/musica/musica-estilos/folclore-vallegrandino': 26,
  '/cine-musica-fotos/videos/videos-generos/drama': 15,
  '/cine-musica-fotos/musica/musica-estilos/pop': 14,
  '/cine-musica-fotos/musica/musica-estilos/rock': 12,
  '/hogar/mascotas-hogar/medicamentos-veterinaria': 8,
  '/cine-musica-fotos/musica/musica-estilos/folclore': 8,
  '/cine-musica-fotos/musica/musica-formatos/video': 7,
  '/cine-musica-fotos/musica/musica-estilos/instrumental': 4,
  '/cine-musica-fotos/musica/musica-estilos/metal': 3,
  '/cine-musica-fotos/musica/musica-estilos/jazz': 3,
  '/cine-musica-fotos/videos/videos-formato/videos-streaming': 2,
  '/cine-musica-fotos/musica/musica-estilos/blues': 2,
  '/cine-musica-fotos/musica/musica-estilos/hip-hop': 2,
  '/cine-musica-fotos/musica/musica-estilos/funk': 2
}

product_total = sum(categories.values())
print(f"The sum is: {product_total}"),
