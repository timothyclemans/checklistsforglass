var checklist = [];
var previewI = 0;
var full_checklist = [];
var status = 'normal';
var currentPreview = [];
var complex_location = [0];
Array.prototype.last = function() {
    return this[this.length-1];
}

function updateDebug() {

}

function processItem(item) {
    
    status = 'normal';
    $('#preview_controls').html('<input type="button" id="wink" value="Wink/Tap to go the next step" />');
    //console.log('Item: '+JSON.stringify(item));
    $('#countdown').remove(); 
    if (item['type'] == 'decision_point') {
        location[location.length-1] += 1;
        $('#preview_controls').html('<input type="button" id="wink" value="Wink/Tap to go the next answer" /><input type="button" id="double_wink" value="Double wink/Two tap to select this answer" />');
        status = 'question';
        previewAnswers = Object.keys(item['acceptable_answers']);
        previewAnswerI = 0;
        $('#preview').html('<strong>Question:</strong> '+item['question']+'<br/><br/><strong>Answer:</strong> <span id="answer">'+previewAnswers[0]+'</span>');
        status = 'question';
        
    } else if (item['type'] == 'goto') {
        //console.log('goto: '+unescape(item['location']));
        processItem(eval(unescape(item['location'])));
        var re = new RegExp("\[\d+\]");
        //console.log('matches: '+unescape(item['location']).match(/\[\d+\]/g));
        var index = unescape(item['location']).match(/\[\d+\]/g)
        index = index.last();
        index = parseInt(index.match(/\d+/g).last());
        //console.log('index: '+index);
        var length = unescape(item['location']).match(/\[\d+\]/g).last().length;
        var whatWillBeCurrent = unescape(item['location']).slice(0, unescape(item['location']).length - length);
        currentPreview = eval(unescape(item['location']).slice(0, unescape(item['location']).length - length));
        previewI = index;
        //alert(previewI);
        //console.log('what will be current: '+whatWillBeCurrent);
        
        //currentPreview = checklist;
        //previewI = 1;
    } else if (item['type'] == 'countdown') {
        $('body').append('<p id="countdown" style="position:absolute; bottom:40px; right:40px;font-size:40px;">'+item['start']+'</p>');
        $('#text').text(currentPreview[previewI]['text']);
        WS.say(currentPreview[previewI]['text']);
        i += 1;
        
    } else if (item['type'] == 'two_part_loop') {
        global_item = item;
        $('body').append('<p id="countdown" style="position:absolute; bottom:40px; right:40px;font-size:40px;">'+item['countdown']+' seconds '+item['countdown_text']+'</p>');
        $('#text').text(currentPreview[previewI]['text']);
        WS.say(currentPreview[previewI]['text']);
        i += 1;
        seconds = item['countdown'];
        beats = true;
        
        setTimeout(function() {beats = false;WS.say('Stop compressions and give two respirations'); $('#text').text('Stop compressions and give two respirations');status='start_main_loop';},30000)
        setInterval(function() {if (beats) { WS.sound('SUCCESS'); }},600);
        setInterval(function() {
            if (seconds == 0) {
                status = 'ask_end_loop_question';
                beats = false;
                seconds = -1;
                WS.say(item['at_end']);
                $('#text').text(item['at_end']);
            } else if (seconds > 0) {
                seconds -=1;$('#countdown').text(seconds+' seconds '+item['countdown_text']);
            }
            
        },1000);
    } else if (item['type'] == 'open_ended_question') {
        //console.log('static text: '+JSON.stringify('
        //console.log('static do: '+currentPreview[previewI]["text"]);
        if (device_type == 'glass') {
            WS.speechRecognize(item['question'], function (data) {advance()});
        } else {
            $('#preview').text('On Glass this is the open ended question: '+item["question"]);
        }
        //$('#text').text(currentPreview[previewI]['text']);
        //WS.say(current[previewI]['text']);
        location[location.length-1] += 1;
        //previewI += 1;
        //advance();
        
    } else if (item['type'] == 'static') {
        //console.log('static text: '+JSON.stringify('
        //console.log('static do: '+currentPreview[previewI]["text"]);
        $('#preview').text(item['text']);
        //$('#preview').text(currentPreview[previewI]["text"]);
        //$('#text').text(currentPreview[previewI]['text']);
        //WS.say(current[previewI]['text']);
        location[location.length-1] += 1;
        //previewI += 1;
        
    }
}
function advance() {
    console.log('start');
    console.log('status: '+status);
    //console.log('advance');
    if (status == 'start_main_loop') {
        console.log('step1: start main loop');
        setTimeout(function() {beats = false;WS.say('Stop compressions and give two respirations'); $('#text').text('Stop compressions and give two respirations');status='start_main_loop';},30000)
        beats = true;
        $('#text').text(global_item['continue']);
        //WS.say(global_item['continue']);
    } else if (status == 'question') {
        console.log('step1: question');
        previewAnswerI += 1;
        
        if (previewAnswerI == previewAnswers.length) {
            previewAnswerI = 0;
        }
       $('#answer').text(previewAnswers[previewAnswerI]);
       status = 'question';
    } else if (status == 'ask_end_loop_question') {
        console.log('step1: ask_end_loop_question');
        status = '';
        //WS.speechRecognize('Is the patient moving?', function (data) {
        //    if (data.toLowerCase() == 'yes') {
        //        $('#text').text('done');
        //    } else {
        //        processItem(current[0]);
         //   
         //   }
            
       // });   
    } else {
        console.log('current preview: '+currentPreview);
        previewI += 1;
        //alert(previewI + ' ' + currentPreview.length + JSON.stringify(currentPreview));
        console.log('step1: else');
        //console.log('current preview: '+JSON.stringify(currentPreview));
        if (previewI < currentPreview.length) {
            //alert('step: previewI < currentPreview.length');
            //console.log('step: previewI < currentPreview.length');
            processItem(currentPreview[previewI]);
            complex_location[complex_location.length - 1] += 1; 
            //alert(complex_location);
            //previewI += 1;
            
        } else if (previewI == currentPreview.length || currentPreview[previewI] == null || currentPreview.length == 0) {
            //alert(previewI + ' ' + currentPreview.length + JSON.stringify(currentPreview));
            //alert('step: previewI == currentPreview.length');
            //console.log('step: previewI == currentPreview.length');
            //alert('same');
            if (complex_location.length > 1) {
                console.log('complex location json: '+JSON.stringify(complex_location));
                //alert('complex location: '+JSON.stringify(complex_location));
                if (complex_location.length < 3) {
                complex_location.pop();
                } else {
                complex_location.pop();
                complex_location.pop();
                }
                if (complex_location.length != 1) {
                previewI = complex_location.pop();
                } else {
                previewI = complex_location[0];
                }
                
                //alert('complex location: '+JSON.stringify(complex_location));
                complex_location_str = 'checklist';
                for (var n=0;n<complex_location.length-1;n++) {
                    if (n % 2 == 0) {
                        complex_location_str += '['+complex_location[n]+']';
                    } else {
                        complex_location_str += '["acceptable_answers"]["'+complex_location[n]+'"]';
                    }
                }
                console.log('complex location string: '+complex_location_str);
                //alert('complex location: '+complex_location_str);
                
                currentPreview = eval(complex_location_str);
                //previewI -= 1;
                
                advance();
                //processItem(eval(complex_location_str));
                //currentPreview = eval(complex_location_str);
                
                //previewI = complex_location + 1;
                //alert(JSON.stringify(currentPreview[previewI]));
                //processItem(currentPreview[previewI]);
            } else {
                $('#preview').text('end of checklist');
                //if (device_type == 'glass') {
                //    setTimeout(function() {  WS.shutdown(); }, 2000);
                //}
            }
        }
        
    }
    console.log('status: '+status);
    updateDebug();
    console.log('stop');
}
function select() {
    status = 'normal';
    updateDebug();
    $('#answered_questions').append('<strong>'+currentPreview[previewI]['question']+'</strong> '+$('#answer').text()+'<br/>');
    //console.log(JSON.stringify(currentPreview));
    if (currentPreview[previewI]['acceptable_answers'][$('#answer').text()].length > 0) {
        //alert('this is where the problem is');
        if (complex_location.length != 1) {
            complex_location.push(previewI);
        }
        complex_location.push($('#answer').text());
        
        currentPreview = currentPreview[previewI]['acceptable_answers'][$('#answer').text()];
        previewI = 0;
        //previewI += 1;
        
        processItem(currentPreview[previewI]);
        updateDebug();
    } else {
        var complex_location_str = 'checklist';
        console.log('complex location json: '+JSON.stringify(complex_location));
        for (var n=0;n<complex_location.length-1;n++) {
                    if (n % 2 == 0) {
                        complex_location_str += '['+complex_location[n]+']';
                    } else {
                        complex_location_str += '["acceptable_answers"]["'+complex_location[n]+'"]';
                    }
                }
                console.log('complex location string: '+complex_location_str);
        currentPrevew = checklist;
        previewI = complex_location[0];
        
        advance();
        //(checklist[0]);
        updateDebug();
        //advance();
        //previewI += 1;
        
        //processItem(currentPreview[previewI]);
    }
    
    updateDebug();
}
