function printPage() { 
            var divContents = document.getElementById("GFG").innerHTML; 
            var a = window.open('', '', 'height=1754, width=1240'); 
            a.document.write('<html>'); 
            a.document.write('<body style"font-size:100% !important;">'); 
            a.document.write(divContents); 
            a.document.write('</body></html>'); 
            a.document.close(); 
            a.print(); 
        } 
