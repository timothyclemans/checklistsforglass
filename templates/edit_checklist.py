<html>
<head>
<title></title>
<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
<script>



function showUnregisteredDevices() {
    $.get('/unregistered_devices/', function (data) { 
       $('ul').html('');
       for (var i = 0; i<data.length; i++) {
           $('ul').append('<li><input type="button" value="'+data[i]+'" /></li>');
       }
       setTimeout(function() { showUnregisteredDevices(); }, 10000);
    });
}
$(function() {
    showUnregisteredDevices();
    $('body').on('click', ':button', function() {
    alert('done');
    $('body').css({'background': 'green'});
    $.get('/register_device/'+$(this).val()+'/');
});
});
</script>
</head>
<body>
<h1>Checklists for Glass</h1>
<h2>Edit checklist</h2>
<strong>Name:</strong> <input type="text" value="{{ checklist.name }}" />
</body>
</html>
