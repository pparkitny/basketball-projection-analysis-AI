function ekUpload(){
    function Init() {
  
      console.log("Upload Initialised");
  
      var fileSelect    = document.getElementById('file-upload'),
          fileDrag      = document.getElementById('file-drag'),
          submitButton  = document.getElementById('submit-button');
  
      fileSelect.addEventListener('change', fileSelectHandler, false);
  
      // Is XHR2 available?
      var xhr = new XMLHttpRequest();
      if (xhr.upload) {
        // File Drop
        fileDrag.addEventListener('dragover', fileDragHover, false);
        fileDrag.addEventListener('dragleave', fileDragHover, false);
        fileDrag.addEventListener('drop', fileSelectHandler, false);
      }
    }
  
    function fileDragHover(e) {
      var fileDrag = document.getElementById('file-drag');
  
      e.stopPropagation();
      e.preventDefault();
  
      fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
    }
  
    function fileSelectHandler(e) {
      // Fetch FileList object
      var files = e.target.files || e.dataTransfer.files;
  
      // Cancel event and hover styling
      fileDragHover(e);
  
      // Process all File objects
      for (var i = 0, f; f = files[i]; i++) {
        parseFile(f);
        uploadFile(f);
      }
    }
  
    // Output
    function output(msg) {
      // Response
      var m = document.getElementById('messages');
      m.innerHTML = msg;
    }
  
    function parseFile(file) {
  
      console.log(file.name);
      output(
        '<div style="display: flex;flex-direction: column;justify-content: center;"> <strong style="margin-bottom: 20px;">' + encodeURI(file.name) + '</strong>' +  '<div id="loader"> <div class="preloader-wrapper active"> <div class="spinner-layer spinner-yellow-only"> <div class="circle-clipper left"> <div class="circle"></div> </div><div class="gap-patch"> <div class="circle"></div> </div><div class="circle-clipper right"> <div class="circle"></div> </div> </div> </div> </div> </div>'
      );
      
      // var fileType = file.type;
      // console.log(fileType);
      var imageName = file.name;
  
      var isGood = (/\.(?=mp4)/gi).test(imageName);
      if (isGood) {
        document.getElementById('start').classList.add("hidden");
        document.getElementById('response').classList.remove("hidden");
        document.getElementById('notimage').classList.add("hidden");
        // Thumbnail Preview
      }
      else {
        document.getElementById('notimage').classList.remove("hidden");
        document.getElementById('start').classList.remove("hidden");
        document.getElementById('response').classList.add("hidden");
        document.getElementById("file-upload-form").reset();
      }
    }
  
    function setProgressMaxValue(e) {
      var pBar = document.getElementById('file-progress');
  
      if (e.lengthComputable) {
        pBar.max = e.total;
      }
    }
  
    function updateFileProgress(e) {
      var pBar = document.getElementById('file-progress');
  
      if (e.lengthComputable) {
        pBar.value = e.loaded;
      }
    }
  
    function uploadFile(file) {
      console.log(file)
      var xhr = new XMLHttpRequest(),
        fileInput = document.getElementById('class-roster-file'),
        pBar = document.getElementById('file-progress'),
        fileSizeLimit = 1024; // In MB
      if (xhr.upload) {
        // Check if file is less than x MB
        if (file.size <= fileSizeLimit * 1024 * 1024) {
          // Progress bar
          pBar.style.display = 'inline';
          // xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
          // xhr.upload.addEventListener('progress', updateFileProgress, false);
  
          // File received / failed
          xhr.onreadystatechange = function(e) {
            if (xhr.readyState == 4) {
              var response = JSON.parse(xhr.response)
                if(response.task_id){
                  checkStatus(response.task_id)
                }
                else
                {
                  alert(response.error)
                }


            }
          };
  
          // Start upload
          xhr.open('POST', document.getElementById('file-upload-form').action, true);
          xhr.setRequestHeader('X-File-Name', file.name);
          xhr.setRequestHeader('X-File-Size', file.size);
          // xhr.setRequestHeader('Content-Type', 'multipart/form-data');
          var fd = new FormData();
          fd.append("filename", file.name);
          fd.append("csrfmiddlewaretoken", $("#file-upload-form").children().first().val())
          fd.append("drive_file", file);
          xhr.send(fd);

        } else {
          output('Please upload a smaller file (< ' + fileSizeLimit + ' MB).');
        }
      }
    }
  
    // Check for the various File API support.
    if (window.File && window.FileList && window.FileReader) {
      Init();
    } else {
      document.getElementById('file-drag').style.display = 'none';
    }
  }
  ekUpload();

  function checkStatus(task_id){
    $.ajax({
      type: "GET",
      url: "status/" + task_id.toString() + "/",
      success: function(response){
        if(response.state == 'PROGRESS')
        {
          var progress = parseInt(response.step)/parseInt(response.max)
          if($("#file-progress").attr("max") != parseInt(response.max))
          {
            $("#file-progress").attr("max", parseInt(response.max))
          }
          
          $("#file-progress").val(parseInt(response.step))
          $("#file-progress-procent").val(Math.round(progress * 100))
          setTimeout(()=>{
            checkStatus(task_id)
          }, 1000)
        }
        else if(response.state == "SUCCESS")
        {
          console.log(response.result)
          console.log(JSON.stringify(response.result))
          $("#file-progress").val($("#file-progress").val() + 1)

          if (Object.keys(response.result).includes("Film się nie nadaje")) {
            alert("Film nie spełnia podanych kryteriów")
          }
          else {
            AnalysisDone(response.result)
          }
        }
        else if(response.state == "FAILURE"){
          alert(response.step)
          $("#file-progress").val(1)
        }
        else
        {
          setTimeout(()=>{
            checkStatus(task_id)
          }, 1000)
        }
        
      }
    })
  }