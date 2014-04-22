var user_id;
var checklist_id;
var device_type = 'glass';
function onGesture(name) {
    WS.log('gesture: '+name);
    if (name == 'TAP' || name == 'WINK') {
        WS.log('tap');
        advance();
    } else if (name == 'TWO_TAP' || name == 'DOUBLE_BLINK') {
        select();
        
    } else if (name == 'THREE_TAP') {
        start();
    }
    
} 
function getUserId() {
    if (localStorage["checklistsforglass.user_id"] == undefined) {
        WS.qr(function(data) { localStorage["checklistsforglass.user_id"] = data});
    } 
    user_id = localStorage["checklistsforglass.user_id"];
}
function start() {
    getUserId();
    if (localStorage["checklistsforglass.show_tutorial"] != "false") {
        localStorage["checklistsforglass.show_tutorial"] = "false";
        checklist = eval($.ajax({url: 'http://checklistsforglass.com/get_full_checklist/68/', async: false}).responseText);
        currentPreview = checklist;
        //console.log('checklist '+checklist);
        processItem(checklist[0]);
    } else {
        WS.speechRecognize('Name of checklist', function (data) {
            WS.log('name of checklist '+data);
            WS.log($.ajax({url: "http://checklistsforglass.com/get_users_checklists/13/", async: false}).responseText);
            //checklists = {"Care Cards: Heat Stroke": 51, "Nursing note": 60, "Catheter/tube Insertion/Assessment": 2, "Room clean": 41, "Bradycardia Algorithm": 58, "Care Cards: Hypoglycemia": 42, "Health cards": 35, "Nursing: Assessment Neuro(beginner version/student)": 28, "Nursing Assessment Pulmonary(beginner/student)": 32, "Care Cards: Insect bite": 37, "Chest discomfort suggestive of ischemia protocol.": 59, "Nursing quick assessment": 61, "Nursing: Assessment Reproductive(beginner/student)": 48, "ACLS": 16, "Dr Ryan note": 34, "Care Cards: Stroke": 50, "Vitals": 13, "Catheter": 19, "Care Cards: Wound cleansing": 49, "Nursing: sub-set breath sounds location(beginner/student)": 33, "Paramedic IV Start documentation": 4, "Verify Drug order": 54, "Nursing: Assessment Wound(beginner/student)": 31, "ATLS": 17, "BLS": 15, "Research Steps": 66, "Post-Op note": 64, "Care Cards: Allergic RXN": 36, "Refill": 55, "Nursing: Assessment Integumentary(beginner/student)": 30, "Nursing: Assessment Urinary(beginner/student)": 47, "STEMI Fibrinolytic Checklist": 56, "Nursing: Assessment Cardiac/Circulatory(beginner/student)": 43, "Nursing: Assessment M/S(beginner/student)": 29, "Care Cards:Seizure": 40, "Nursing: Med admin": 24, "Pain assessment": 67, "static iv checklists": 45, "Care Cards: Bleeding": 38, "Nursing: Assessment Abdominal(beginner/student)": 46, "Take photo": 76};
            //eval('checklists = '+$.ajax({url: "http://checklistsforglass.com/get_users_checklists/13/", async: false}).responseText);
            eval('checklists = '+$.ajax({url: "http://checklistsforglass.com/get_all_checklists/", async: false}).responseText);
            //var data = 'wound';
            //WS.log('checklists: '+JSON.stringify(checklists));
            var fuzzy_names = FuzzySet(Object.keys(checklists));
            
            var fuzzy_match = fuzzy_names.get(data)[0][1];
            checklist_id = checklists[fuzzy_match];
            WS.log('id: '+checklist_id);
            //var checklist_index = names.indexOf(fuzzy_match);
            //var checklist = checklists[checklist_index];
            checklist = eval($.ajax({url: 'http://checklistsforglass.com/get_full_checklist/'+checklist_id+'/', async: false}).responseText);
            currentPreview = checklist;
            //console.log('checklist '+checklist);
            processItem(checklist[0]);
        });
    }
}
