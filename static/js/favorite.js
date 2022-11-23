//$(document).on('submit','#addFavoriteForm',function(event){
//    event.preventDefault();{
//        // Отправляем AJAX запрос на сервер
//        $.ajax({
//            type: "GET",
//            url: "../../hotel/favorite",
//            data: {
//                'realty_id': obj,
//            },
//            dataType: "text",
//            cache: false,
//
//            success: function (data) {
//                $('.realty_list__favorite_container').form(data);
//            }
//        });
//    };
//}

console.log('СУКАААААААААААААААААААААа')
$(document).ready(
  $('#addFavoriteForm').click(function(e){
    e.preventDefault();
    var serializedData = $(this).serialize();
    $.ajax({
      type:"GET",
      url: "../../hotel/favorite",
      data: {"realty_id": obj},
      success: function(data){
        $("#addFavorite").html(data);
      },
    });
  })
);

//$(document).on('submit','#addFavoriteForm',function(event){
//    event.preventDefault();{
//    // Отправляем AJAX запрос на сервер
//    $.ajax({
//        type: "GET",
//        url: "../../hotel/favorite",
//        data: {
//            'realty_id': obj,
//        },
//        dataType: "text",
//        cache: false,
//
//        success: function (data) {
//            $('.realty_list__favorite_container').form(data);
//        }
//    });
//}
//})