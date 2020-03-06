/* Most of this code was extracted from "Flask Multi Upload Demo" */

// var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
var UPLOAD_URL = "upload_file_a";
var NEXT_URL = "/";
// var NEXT_URL   = "/files/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];
var STORED_FILENAMES = [];
var DUPLICATED_FILES = [];
var NOT_ALLOWED_FILES = [];
var MAX_FILESIZE = 0;
var CATEGORIA_ACTUAL = "";

$(document).ready(function() {
  
  // current category
  CATEGORIA_ACTUAL = document.getElementById('categoria_actual').innerHTML;
  if (CATEGORIA_ACTUAL == 'Misc') {
    UPLOAD_URL = '/Misc/upload_file_a';
  }

  var testExp = new RegExp('Android|webOS|iPhone|iPad|' +
    		           'BlackBerry|Windows Phone|'  +
    		           'Opera Mini|IEMobile|Mobile' , 
    		           'i');
  // console.log('>>>', navigator.userAgent, '::', testExp.test(navigator.userAgent));
  var deviceType = 'desktop';
  if (testExp.test(navigator.userAgent)) {
    deviceType = 'mobile';
  }

  // checking mobile devices
  if (deviceType == 'mobile') {
    // quitando propiedad multiple de file-picker para que haya mas soporte en dispositivos móviles
    $('#file-picker')[0].multiple = false;

    $("#upload-button").on("click", function(e) {
      e.preventDefault();
      mostrarModalSubir();
    });

    $("#upload-button-modal").on("click", function(e) {
      e.preventDefault();
      doUpload(deviceType);
    });
  }

  ocultarModalSubir();
  // Set up the drag/drop zone.
  initDropbox(deviceType);

  // Set up the handler for the file input box.
  $("#file-picker").on("change", function() {
    handleFiles(this.files);
  });

  // Para el modal
  var closeModalSubir = document.getElementById("closeModalSubir");
  var closeModalPassword = document.getElementById("closeModalPassword");
  var modalSubir = document.getElementById("modal-subir");
  var modalPassword = document.getElementById("modal-pass");

  if (deviceType != 'mobile') {
    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
      // If the user has JS disabled, none of this code is running but the
      // file multi-upload input box should still work. In this case they'll
      // just POST to the upload endpoint directly. However, with JS we'll do
      // the POST using ajax and then redirect them ourself when done.
      e.preventDefault();

      // When the user clicks on the button, open the modal
      mostrarModalSubir();
      // funcion subir
      doUpload(deviceType);
    });
  }

  // cerrar el modal
  closeModalSubir.onclick = function() {
    ocultarModalSubir();
  };

  closeModalPassword.onclick = function() {
    ocultarModalPassword();
  };

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modalSubir) {
      ocultarModalSubir();
    }
    if (event.target == modalPassword) {
      ocultarModalPassword();
    }
  };

  // descargar de archivos protegidos
  $("#download_protected")
    .submit(function(event) {
      event.preventDefault();
      var post_url = $(this).attr("action"); //get form action url
      var request_method = $(this).attr("method"); //get form GET/POST method

      // parece que jquery tiene errores con las respuestas blob de archivos grandes, por eso se usa XMLHTttpRequest
      var request = new XMLHttpRequest();
      request.open(request_method, post_url, true);
      request.responseType = 'blob';
      
      request.onload = function() {
        if (request.status == 200) {
          var filename = document.getElementById("nombre_archivo_protegido_label").innerHTML;
          $("#pwd_msj_download").html('');
          var blob = new Blob([request.response], { type: 'application/download' });          
          var link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = filename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } else {
          // TODO: convertir a objeto por que la respuesta de error es de tipo JSON
          //console.log(request.response);
          $("#pwd_msj_download").html('&#x2715; Contraseña incorrecta');
        }
      };
      var form_data = new FormData(document.getElementById('download_protected'));
      request.send(form_data);
    });

  // prevenir ir al enlace por defecto (solo funciona si javascript esta activo)
  document.getElementsByName("enlace_archivo_protegido").forEach(e => {
    e.href = "javascript:void(0);";
  });
    //   $.ajax({
    //     url: post_url,
    //     type: request_method,
    //     data: form_data,
    //   }).
    //     done(function(response, textStatus, request) {
    //       // respuesta correcta creando un enlace para descargar el archivo
    //       $("#pwd_msj_download").html('');

    //       // The actual download
    //       // source solution: https://nehalist.io/downloading-files-from-post-requests/

    //       var blob = new Blob([request.response], { type: 'application/download' });
    //       var link = document.createElement('a');
    //       link.href = window.URL.createObjectURL(blob);
    //       var filename = document.getElementById("nombre_archivo_protegido_label").innerHTML;
    //       link.download = filename;
    //       document.body.appendChild(link);
    //       link.click();
    //       document.body.removeChild(link);
    //     }).
    //     error(function(response) {
    //       $("#pwd_msj_download").html(response.responseJSON.error.msj);
    //     });
      // });

});


function initDropbox(deviceType) {
  var $dropbox = $("#dropbox");
  var $listaSubir = $('#lista_archivos_subir');
  
  if (deviceType === 'mobile') {
    $dropbox.html('Arrastra tu archivo aquí');
  }
  // On drag enter...
  $dropbox.on("dragenter", function(e) {
    e.stopPropagation();
    e.preventDefault();
    $(this).addClass("active");
  });

  // On drag over...
  $dropbox.on("dragover", function(e) {
    e.stopPropagation();
    e.preventDefault();
  });

  // On drop...
  $dropbox.on("drop", function(e) {
    e.preventDefault();
    $(this).removeClass("active");

    // cleaning arrays
    PENDING_FILES.splice(0);
    DUPLICATED_FILES.splice(0);
    
    // Get the files.
    var files = e.originalEvent.dataTransfer.files;
    handleFiles(files);

    // Update the display to acknowledge the number of pending files.
    var texto = "";
    for (var i = 0; i < PENDING_FILES.length ; i++) {
      texto += "&check;" + PENDING_FILES[i].name + " (<b>" +PENDING_FILES[i].size +"</b> bytes)<br>";
    }
    for (let i = 0; i < DUPLICATED_FILES.length; i++) {
      texto += "&#x2715;" + DUPLICATED_FILES[i].name + " (duplicado)<br>";
    }

    mostrarModalSubir();
    $listaSubir.html(texto + "<br/><big><b>"+PENDING_FILES.length+"</big></b> archivos.");
  });

  // If the files are dropped outside of the drop zone, the browser will
  // redirect to show the files in the window. To avoid that we can prevent
  // the 'drop' event on the document.
  function stopDefault(e) {
    e.stopPropagation();
    e.preventDefault();
  }
  $(document).on("dragenter", stopDefault);
  $(document).on("dragover", stopDefault);
  $(document).on("drop", stopDefault);

  // getting STORED_FILENAMES
  var storedFiles = document.getElementById('caja_archivos');
  var filenames = storedFiles.getElementsByTagName('a');
  
  for (var i=0; i<filenames.length; i++){
    STORED_FILENAMES.push(filenames[i].text);
  }
}

function mostrarModalSubir(deviceType) {
  var modalSubir = document.getElementById("modal-subir");
  modalSubir.style.display = "block";
}

function mostrarModalPassword(nombre) {
  var modalPassword = document.getElementById("modal-pass");
  modalPassword.style.display = "block";
}

function ocultarModalPassword(nombre) {
  var modalPassword = document.getElementById("modal-pass");
  modalPassword.style.display = "none";
}

function ocultarModalSubir(deviceType) {
  var modalSubir = document.getElementById("modal-subir");
  var dom_passwordCheck = document.getElementById('pwd_check');
  modalSubir.style.display = "none";
  dom_passwordCheck.checked = false;
  menuPassword();
  PENDING_FILES = [];
  DUPLICATED_FILES = [];
  NOT_ALLOWED_FILES = [];
}

function doUploadModal() {
  doUpload('');
}

function doUpload(deviceType) {
  // comprobando password
  if (passwordCheck()) {
    if (comprobarPasswords()) {
      $('#pwd_msj').html(' ');
    } else {
      $('#pwd_msj').html('&#x2715; contraseñas muy cortas o no coinciden');
      return;
    } 
  }

  $("#progress").show();
  var $progressBar = $("#progress-bar");
  var $estadoRecepcion = $("#estado-recepcion");

  var $caja_archivos = $("#caja_archivos");
  
  // Gray out the form.
  $("#upload-file :input").attr("disabled", "disabled");

  // Initialize the progress bar.
  $progressBar.css({"width": "0%"});

  // Collect the form data.
  var fd = collectFormData();

  // Attach the files.
  for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
    // Collect the other form data.
    fd.append("file", PENDING_FILES[i]);
  }

  // Inform the back-end that we're doing this over ajax.
  fd.append("__ajax", "true");

  if (passwordCheck()) {
    var pwd1 = document.getElementById('pwd1');
    fd.append('password', pwd1.value);
  }

  // peticion subir archivo(s)
  var xhr = $.ajax({
    xhr: function() {
      var xhrobj = $.ajaxSettings.xhr();
      if (xhrobj.upload) {
        xhrobj.upload.addEventListener("progress", function(event) {
          var percent = 0;
          var position = event.loaded || event.position;
          var total = event.total;
          if (event.lengthComputable) {
            percent = Math.ceil(position / total * 100);
          }
          // Set the progress bar.
          $progressBar.css({"width": percent + "%"});
          $progressBar.text(percent + "% enviado");
	  if (percent == 100) {
	    $estadoRecepcion.text("Comprobando archivo(s)...");
          }
        }, false);
      }
      return xhrobj;
    },
    url: UPLOAD_URL,
    method: "POST",
    contentType: false,
    processData: false,
    cache: false,
    data: fd,
    success: function(data) {
      console.log('respuesta:::', data);
      $progressBar.css({"width": "100%"});
      $estadoRecepcion.text("Guardando archivo(s) en el servidor ...");
      // data = JSON.parse(data);

      // inspeccionando y actualizando respuesta
      var texto = '';
      if (data.exitosos.length > 0) {
        for (let i = 0; i < data.exitosos.length; i++) {
          texto += "<big>&check;</big> <b>" + data.exitosos[i] + "</b><br>";
        }
      }
      if (data.erroneos.length > 0) {
        for (let i = 0; i < data.erroneos.length; i++) {
          texto += "&#x2715; " + data.erroneos[i].redirect + "(" + data.erroneos[i].mensaje + ")<br>";
        }
      }
      // console.log('texto', texto);
      var $dropbox = $('#dropbox');
      $dropbox.html('');
      $dropbox.html(texto);
      
      $("#lista_archivos_subir").html(texto);
      
      setTimeout(function() {
        ocultarModalSubir();
        location.reload();
      }, 1500);
      /*
      // How'd it go?
      if (data.status === "error") {
        // Uh-oh.
        window.alert(data.msg);
        $("#upload-file :input").removeAttr("disabled");
        return;
      }
      else {
	// Ok
	var delayInMilliseconds = 1000; //1 second

	setTimeout(function() {
	  // luego del reatardo se recarga la pagina
	  location.reload(true);
	}, delayInMilliseconds);

	// redirection
	//window.location = NEXT_URL;
      }
       */
    },
  });
}

function collectFormData() {
  // Go through all the form fields and collect their names/values.
  var fd = new FormData();

  console.log('collectFormData...');
  $("#upload-file :input").each(function() {
    var $this = $(this);
    var name  = $this.attr("name");
    var type  = $this.attr("type") || "";
    var value = $this.val();
    console.log(`name: ${name}\nvalue:${value}---'n`);
    // No name = no care.
    if (name === undefined) {
      return;
    }

    // Skip the file upload box for now.
    if (type === "file") {
      return;
    }
    
    fd.append(name, value);
  });

  return fd;
}

function handleFiles(files) {
  var fs = document.getElementById('max_filesize');
  MAX_FILESIZE = parseInt(document.
			  getElementById('max_filesize').
			  innerText);
  
  // Add them to the pending files list.
  for (var i = 0, ie = files.length; i < ie; i++) {
    // checking for duplicated files and max filesize
    if (files[i].size >= MAX_FILESIZE) {
      NOT_ALLOWED_FILES.push(files[i]);
    } else if (STORED_FILENAMES.indexOf(files[i].name) == -1){
      PENDING_FILES.push(files[i]);
    } else {
      DUPLICATED_FILES.push(files[i]);
    }
  }
}

function actualizarArchivosSubir(files) {
  var $listaSubir = $('#lista_archivos_subir');
  handleFiles(files);

  var texto = "";
  for (var i = 0; i < PENDING_FILES.length ; i++) {
    texto += "&check;" + PENDING_FILES[i].name + " (<b>" +PENDING_FILES[i].size +"</b> bytes)<br>";
  }
  for (let i = 0; i < DUPLICATED_FILES.length; i++) {
    texto += "&#x2715;" + DUPLICATED_FILES[i].name + " (duplicado)<br>";
  }
  for (let i = 0; i < NOT_ALLOWED_FILES.length; i++) {
    texto += "&#x2757;" + NOT_ALLOWED_FILES[i].name + " (<b>" + NOT_ALLOWED_FILES[i].size + "</b> bytes) tamaño excedido<br>";
  }
  mostrarModalSubir();
  $listaSubir.html(texto + "<br/><big><b>"+PENDING_FILES.length+"</big></b> archivos.");
}

function passwordCheck() {
  return document.getElementById("pwd_check").checked;
}

function menuPassword() {
  var menuPassword = document.getElementById("menu_password");
  if (passwordCheck() == true) {
    menuPassword.style.display = 'block';
  } else {
    menuPassword.style.display = 'none';
  }
}

function comprobarPasswords() {
  var pwd1 = document.getElementById("pwd1");
  var pwd2 = document.getElementById("pwd2");
  if (pwd1.value === pwd2.value && pwd1.value.length > 0) {
    return true;
  }
  return false;
}

function descargarProtegido(nombre) {
  var archivoProtegido = document.getElementById("nombre_archivo_protegido");
  archivoProtegido.value = nombre;
  document.getElementById("nombre_archivo_protegido_label").innerHTML = nombre;
  mostrarModalPassword(nombre);
}

function copiarEnlace(str) {
  // solution extracted from: https://hackernoon.com/copying-text-to-clipboard-with-javascript-df4d4988697f
  var loc = decodeURI(document.URL);
  var domain = '';
  var texto = '';
  if (CATEGORIA_ACTUAL == 'Misc') {
    // caso especial
    texto = loc + 'almacen/' + CATEGORIA_ACTUAL + '/' + str;
    var arr = loc.split('/');
    if (arr[arr.length - 2] == 'Misc') {
      var ar = arr.splice(0, arr.length-2);
      texto = ar.join('/') + '/almacen/' + CATEGORIA_ACTUAL + '/' + str;
    } else {
      texto = loc + 'almacen/' + CATEGORIA_ACTUAL + '/' + str;      
    }
  } else {
    domain = loc.split('/'+CATEGORIA_ACTUAL)[0];
    texto = domain + '/almacen/'+ CATEGORIA_ACTUAL +'/'+ str;
  }
  // console.log(texto);
  const el = document.createElement('textarea');
  el.value = texto;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);
};
