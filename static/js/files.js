function previewFiles(i, evt){
  var x = document.getElementById("files");
  var txt = "";
  if ('files' in x) {
    if (x.files.length != 0) {
      evt.preventDefault();
      txt += '<div class="file-list">'
      if(i>=x.files.length){i-=3;}
      if(x.files.length<3){j=x.files.length}else{j=i+3;}
      if(j>x.files.length){j=x.files.length}
      if(i<3){k=0}else{k=i-3}
      var pages= Math.ceil(x.files.length/3);
      page= Math.ceil(j/3);
      if(j>=x.files.length){l=i;}else{l=j;}
      ctr=i;
      for (var i; i < j; i++) {
        txt += '<li class="pure-menu-item"><div class="pure-g"><div class="pure-u-1-5"><svg xmlns="http://www.w3.org/2000/svg" width="2.2em" height="2.2em" viewBox="0 0 24 24"><path fill="currentColor" d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8zM6 20V4h7v5h5v11z"/></svg></div>';
        var file = x.files[i];
        if ('name' in file) {
          txt += '<div class="pure-u-3-5">' + file.name.substring(0, 18) + "...<br>";
        }
        if ('size' in file) {
          txt += "<span>size: " + file.size + ' bytes</span></div><div class="pure-u-1-5 erase"><button class="pure-button clear-button" id="files" name="files" onclick="deleteFile(' + i + ',' + ctr + ',event)"><svg xmlns="http://www.w3.org/2000/svg" width="1.8em" height="1.8em" viewBox="0 0 24 24"><path fill="currentColor" d="M18.3 5.71a.996.996 0 0 0-1.41 0L12 10.59L7.11 5.7A.996.996 0 1 0 5.7 7.11L10.59 12L5.7 16.89a.996.996 0 1 0 1.41 1.41L12 13.41l4.89 4.89a.996.996 0 1 0 1.41-1.41L13.41 12l4.89-4.89c.38-.38.38-1.02 0-1.4"/></svg></button></div></div></li>';
        }
      }
      txt += '<li class="pure-menu-item pages"><div class="pure-g"><div class="pure-u-3-5"><p>Showing page ' + page + ' of ' + pages + '</p></div><div class="pure-u-2-5"><button class="pure-button clear-button" id="files" name="files" onclick="previewFiles(' + k + ',event)"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M16.62 2.99a1.25 1.25 0 0 0-1.77 0L6.54 11.3a.996.996 0 0 0 0 1.41l8.31 8.31c.49.49 1.28.49 1.77 0s.49-1.28 0-1.77L9.38 12l7.25-7.25c.48-.48.48-1.28-.01-1.76"/></svg></button><button class="pure-button clear-button" id="files name="files" onclick="previewFiles(' + l + ', event)"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M7.38 21.01c.49.49 1.28.49 1.77 0l8.31-8.31a.996.996 0 0 0 0-1.41L9.15 2.98c-.49-.49-1.28-.49-1.77 0s-.49 1.28 0 1.77L14.62 12l-7.25 7.25c-.48.48-.48 1.28.01 1.76"/></svg></button></div></div></li></div>';
    } 
  } 
  else {
    if (x.value != "") {
      txt += "The files property is not supported by your browser!";
      txt  += "<br>The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead. 
    }
  }
  document.getElementById("filesview").innerHTML = txt;
}
function deleteFile(index, control, event)  {
        const dt = new DataTransfer()
        const input = document.getElementById('files')
        const { files } = input
  
        for (let i = 0; i < files.length; i++) {
        const file = files[i]
        if (index !== i)
            dt.items.add(file) // here you exclude the file. thus removing it.
        }
  
        input.files = dt.files // Assign the updates file-list
        
        previewFiles(control, event)
    }
