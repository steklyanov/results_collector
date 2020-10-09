<template>
  <div>
    <canvas ref="canvas"></canvas>
    <v-btn @click="addNewPolygon('0')"  :color="polygon_types['0'].color">Добавить полигон на {{polygon_types['0'].name}}</v-btn>
    <v-btn @click="addNewPolygon('1')" :color="polygon_types['1'].color"> Добавить полигон на {{polygon_types['1'].name}}</v-btn>
    <v-btn @click="savePolygon()"> Сохранить полигон</v-btn>
  </div>

</template>

<script>
  import "fabric";

  export default {
        name: "ZoneSelector",
      props: ["image_path", "polygon", "camera_id"],
      data: () => ({
        shape_array: [], // Массив полигонов формата fabric
        issueColor: "#D32F2F",
        is_creating: true,
        add_point: false,
        shape: null, // Текущий полигон, его точки, после заврешения редактирования добавляется в массив shape_array
        canvas: null,
        result_array: [], // Сюда скаладываю финальный массив полигонов с типом полигона и валидными точками
        polygon_types: {
          "0": {
            "name": "вьезд",
            "code": "0",
            "color": "rgba(0, 80, 0, 0.3)"
          },
          "1": {
            "name": "выезд",
            "code": "1",
            "color": "rgba(80, 0, 0, 0.3)"
          }
        },
      }),
      image_path: {
        item() {
          this.createPolygons();
          this.transformPolygon()
        }
      },
      mounted() {
        this.createPolygons();
        this.transformPolygon()
      },
      methods: {
          // Метод вызывается перед отправкой полигона на бэк, трансформирует обьект в полигон пригодный для бэка
          savePolygon() {
            this.updateCanvas()
            console.log("RESULT", this.result_array)
            this.$axios
              .post("api/v1/polygon/update/", { "camera_id": this.camera_id, "polygons": this.result_array })
              .then(r => {
                console.log(r)
              });
          },
          // Зануляет переменные для того что-бы создать новый полигон
          addNewPolygon(idx) {
            console.log(idx)
            this.result_array.push({"type": idx})
            this.updateCanvas()
            this.is_creating = false
            this.add_point = true
          },
          // Перерисовывает картинку, добавляет созданный полигон в массив полигонов
          updateCanvas() {
              if (this.is_creating && this.shape) {
                // this.result_array.push({"type": idx})

                let polygon = this.shape.toJSON()
                let polygon_copy = []
                polygon.points.forEach((point) => {
                  polygon_copy.push({
                    "x": point.x * 2,
                    "y": point.y * 2
                  })
                })
                polygon_copy.splice(1, 1)
                this.result_array[this.result_array.length - 1].polygon = polygon_copy



                this.canvas.remove(this.shape);
                this.shape_array.forEach((sh => {
                  this.canvas.remove(sh);
                }))
                this.shape_array.push(this.shape)
                this.shape = null
                this.canvas.add(...this.shape_array)
              }
          },
          //Функция создания полигона
          createPolygons() {
            this.canvas = new fabric.Canvas(this.$refs.canvas);
            fabric.Image.fromURL(this.image_path, img => {
              img.set({
                originX: "left",
                originY: "top",
              });
              this.canvas.setWidth(img.width / 2)
              let ratio = this.canvas.width / img.width;
              let newHeight = Math.round(img.height * ratio);
              img = img.scaleToWidth(this.canvas.width);
              this.canvas.setHeight(newHeight);
              this.canvas.setBackgroundImage(img, this.canvas.renderAll.bind(this.canvas));
            });

            let mouse_dragging, mouseCoords;
            this.canvas.on('mouse:dblclick', (evt) => {
                this.shape_array.forEach(((sh, ind) => {
                  if (sh.containsPoint(evt.absolutePointer)) {
                    this.canvas.remove(sh);
                    this.result_array.splice(ind, 1)
                    this.shape_array.splice(ind, 1);
                  }
                }))
              });
            this.canvas.on('object:moving', (evt) => {
              let matrix = evt.target.calcTransformMatrix()
              let transformedPoints = evt.target.get('points')
                .map((p) => {
                  return new fabric.Point(
                    p.x - evt.target.pathOffset.x,
                    p.y - evt.target.pathOffset.y);
                })
                .map((p) => {
                  return fabric.util.transformPoint(p, matrix);
                });

              this.shape_array.forEach(((sh, idx) => {
                if (sh.containsPoint(evt.pointer)) {
                  let polygon_copy = []
                  transformedPoints.forEach((point) => {
                    polygon_copy.push({
                      "x": point.x * 2,
                      "y": point.y * 2
                    })
                  })
                  polygon_copy.splice(1, 1)
                  this.result_array[idx].polygon = polygon_copy
                }
              }))
            })
            this.canvas.on('object:scaling', (evt) => {
              console.log("SCALING", evt)
              console.log(this.result_array)
              let matrix = evt.target.calcTransformMatrix()
              let transformedPoints = evt.target.get('points')
                .map((p) => {
                  return new fabric.Point(
                    p.x - evt.target.pathOffset.x,
                    p.y - evt.target.pathOffset.y);
                })
                .map((p) => {
                  return fabric.util.transformPoint(p, matrix);
                });

              console.log(evt.target.points)
              this.shape_array.forEach((shape, idx) => {
                if (shape.points[0].x === evt.target.points[0].x) {
                  console.log("Catch it ", idx)
                  let polygon_copy = []
                  transformedPoints.forEach((point) => {
                    polygon_copy.push({
                      "x": point.x * 2,
                      "y": point.y * 2
                    })
                  })
                  polygon_copy.splice(1, 1)
                  this.result_array[idx].polygon = polygon_copy
                }
              })

            })
            this.canvas.on('mouse:down', (evt) => {
                mouse_dragging = true;
                if (this.shape && this.shape.containsPoint(evt.absolutePointer)) {
                  this.add_point = false
                  this.updateCanvas()
                }
              });
            this.canvas.on('mouse:up', (evt) => {
                mouseCoords = {
                  x: this.canvas.getPointer(evt.e, true).x,
                  y: this.canvas.getPointer(evt.e, true).y
                }
                if (this.add_point === true) {
                  if (!this.is_creating) {
                    this.is_creating = true;
                    this.shape = new fabric.Polygon([{
                      x: mouseCoords.x,
                      y: mouseCoords.y
                    }, {
                      x: mouseCoords.x + 1,
                      y: mouseCoords.y + 1
                    }], {
                      // Пацаны простите, когда мы создаем новый полигон, мы записываем в result_array его тип,
                      // по этому типу я могу получить цвет для полигона,
                      fill: this.polygon_types[this.result_array[this.result_array.length - 1].type].color,
                      stroke: 'black',
                      perPixelTargetFind: true,
                      top: mouseCoords.y,
                      left: mouseCoords.x,
                      strokeWidth: 2
                    });
                    this.canvas.add(this.shape);
                  } else {
                    this.shape.points.push({
                      x: mouseCoords.x,
                      y: mouseCoords.y
                    });
                    this.canvas.remove(this.shape);
                    let obj = this.shape.toObject();
                    delete obj.top;
                    delete obj.left;
                    this.shape = new fabric.Polygon(this.shape.points, obj );
                    this.canvas.add(this.shape);
                  }
                }
              this.canvas.renderAll()
              });
          },
          // При получени полигона с бэка трансформирует его в вид для библиотеки fabric
          transformPolygon() {
            if (this.polygon == undefined ){return}
              this.polygon.forEach((poly) => {
                if (poly.point.length === 0) { return }
                console.log(poly, "on create")
                this.result_array.push({"type": poly.type, "polygon": poly.point})
                let shape = new fabric.Polygon([{
                  x: poly.point[0].x / 2,
                  y: poly.point[0].y / 2
                }, {
                  x: poly.point[0].x / 2 + 1,
                  y: poly.point[0].y / 2 + 1
                }], {
                  fill: this.polygon_types[poly.type].color,
                  stroke: 'black',
                  perPixelTargetFind: true,
                  top: poly.point[0].y,
                  left: poly.point[0].x,
                  strokeWidth: 2
                });
                let copied = JSON.parse(JSON.stringify(poly.point))
                copied.shift()
                copied.forEach((point) => {
                  shape.points.push({
                    x: point.x / 2,
                    y: point.y / 2
                  });
                })

                let obj = shape.toObject();
                delete obj.top;
                delete obj.left;
                shape = new fabric.Polygon(shape.points, obj );
                this.canvas.add(shape);

                this.shape_array.push(shape)
              })
            this.updateCanvas()
          }
      }
    };
</script>

<style scoped>

</style>
