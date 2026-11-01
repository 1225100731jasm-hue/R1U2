#!/bin/bash
URL=http://localhost:5000
J="Content-Type: application/json"
date

echo "--- 1. Crear categoria"
curl -i -X POST $URL/categorias -H "$J" -d '{"nombre":"Redes"}'
echo "--- 2. Listar categorias"
curl -s $URL/categorias
echo "--- 3. Ver categoria 1"
curl -i -X GET $URL/categorias/1
echo "--- 4. Actualizar categoria 1"
curl -i -X PUT $URL/categorias/1 -H "$J" -d '{"nombre":"Redes y cables"}'
echo "--- 5. Crear producto 1"
curl -i -X POST $URL/productos -H "$J" -d '{"nombre":"Switch","precio":850.5,"stock":10,"categoria_id":1}'
echo "--- 6. Crear producto 2"
curl -i -X POST $URL/productos -H "$J" -d '{"nombre":"Cable UTP","precio":25,"stock":50,"categoria_id":1}'
echo "--- 7. Ver producto 1"
curl -s $URL/productos/1
echo "--- 8. Actualizar producto 1"
curl -i -X PUT $URL/productos/1 -H "$J" -d '{"nombre":"Switch 24p","precio":900,"stock":10,"categoria_id":1}'
echo "--- 9. Paginacion"
curl -s "$URL/productos?page=1&per_page=1"
echo "--- 10. Filtro por categoria"
curl -s "$URL/productos?categoria=1"
echo "--- 11. Orden descendente por precio"
curl -s "$URL/productos?sort=-precio"
echo "--- 12. Solo codigo de estado"
curl -s -o /dev/null -w "%{http_code}\n" "$URL/productos?page=1&per_page=5"
echo "--- 13. Salida exitosa"
curl -i -X POST $URL/productos/1/salidas -H "$J" -d '{"cantidad":3}'
echo "--- 14. Salida con conflicto (409)"
curl -i -X POST $URL/productos/1/salidas -H "$J" -d '{"cantidad":999}'
echo "--- 15. Error 400 (JSON mal formado)"
curl -i -X POST $URL/productos -H "$J" -d '{mal'
echo "--- 16. Error 404"
curl -i $URL/productos/999
echo "--- 17. Error 422 (precio negativo)"
curl -i -X POST $URL/productos -H "$J" -d '{"nombre":"X","precio":-5,"stock":1,"categoria_id":1}'
echo "--- 18. Error 405"
curl -i -X DELETE $URL/categorias
echo "--- 19. Borrar producto 2"
curl -i -X DELETE $URL/productos/2
echo "--- 20. Crear categoria temporal"
curl -i -X POST $URL/categorias -H "$J" -d '{"nombre":"Temporal"}'
echo "--- 21. Borrar categoria temporal"
curl -i -X DELETE $URL/categorias/2
echo "--- 22. Borrar categoria con productos (409)"
curl -i -X DELETE $URL/categorias/1
