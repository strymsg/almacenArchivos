/* Code extracted from "Flask Multi Upload Demo" */

// var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
var UPLOAD_URL = "upload_file_a";
var NEXT_URL = "/";
// var NEXT_URL   = "/files/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];
var STORED_FILENAMES = [];
var DUPLICATED_FILES = [];
var MAX_FILESIZE = 0;
var CATEGORIA_ACTUAL = "";

$(document).ready(function() {
  // Set up the drag/drop zone.
  initDropbox();
  
  // current category
  
  CATEGORIA_ACTUAL = document.getElementById('categoria_actual').innerHTML;
  // UPLOAD_URL = CATEGORIA_ACTUAL + '/upload_file_a';
  // if (CATEGORIA_ACTUAL != "Misc")
  //   // UPLOAD_URL = "/almacen/"+CATEGORIA_ACTUAL+"/upload_file_a";
  //   UPLOAD_URL = CATEGORIA_ACTUAL+"/upload_file_a";

  console.log('upload URL:', UPLOAD_URL);
  
  // Set up the handler for the file input box.
  $("#file-picker").on("change", function() {
    handleFiles(this.files);
  });

  // Handle the submit button.
  $("#upload-button").on("click", function(e) {
    // If the user has JS disabled, none of this code is running but the
    // file multi-upload input box should still work. In this case they'll
    // just POST to the upload endpoint directly. However, with JS we'll do
    // the POST using ajax and then redirect them ourself when done.
    e.preventDefault();
    doUpload();
  });
});


function doUpload() {
  $("#progress").show();
  var $progressBar   = $("#progress-bar");
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

  var xhr = $.ajax({
    xhr: function() {
      var xhrobj = $.ajaxSettings.xhr();
      if (xhrobj.upload) {
        xhrobj.upload.addEventListener("progress", function(event) {
          var percent = 0;
          var position = event.loaded || event.position;
          var total    = event.total;
          if (event.lengthComputable) {
            percent = Math.ceil(position / total * 100);
          }
          // Set the progress bar.
          $progressBar.css({"width": percent + "%"});
          $progressBar.text(percent + "% enviado");
	  if (percent == 100)
	    $estadoRecepcion.text("Comprobando archivo(s)...");
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
      $progressBar.css({"width": "100%"});
      $estadoRecepcion.text("Guardando archivo(s) en el servidor ...");
      data = JSON.parse(data);
      
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
    },
  });
}


function collectFormData() {
  // Go through all the form fields and collect their names/values.
  var fd = new FormData();
  console.log('fd::::', fd);
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
    if (STORED_FILENAMES.indexOf(files[i].name) == -1 &&
	files[i].size <= MAX_FILESIZE) {
      PENDING_FILES.push(files[i]);
    } else {
      DUPLICATED_FILES.push(files[i]);
    }
  }
}


function initDropbox() {
  var $dropbox = $("#dropbox");

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
      texto += "&check;" + PENDING_FILES[i].name + "<br>";
    }
    for (let i = 0; i < DUPLICATED_FILES.length; i++) {
      texto += "&#x2715;" + DUPLICATED_FILES[i].name + " (duplicado)<br>";
    }
    
    $dropbox.html(texto + "<br/><big><b>"+PENDING_FILES.length+"</big></b> archivos.");
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
