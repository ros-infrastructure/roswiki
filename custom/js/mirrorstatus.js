function setMirrorStatus(link, msg) {
  msg = msg.trim();
  console.log('setMirrorStatus() msg: ' + msg);
  var re = new RegExp('^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$', 'g');
  var isTimestamp = msg.match(re);
  $(link).css('background-color', isTimestamp ? '#5cb85c' : '#f0ad4e');
  $(link).text(msg);
}

function checkMirrorStatus(link, url) {
  console.log('checkMirrorStatus() url: ' + url);
  setMirrorStatus(link, '...');

  // fetch timestamp file from mirror
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url + '/wikidump.timestamp');

  xhr.onreadystatechange = function () {
    if (this.readyState == 4) {
      console.log('checkMirrorStatus() url: ' + url + ', status: ' + this.status);
      if (this.status >= 200 && this.status < 300) {
        setMirrorStatus(link, this.responseText);
      } else if (this.status == 0) {
        // not allowed due to missing Access-Control-Allow-Origin header
        setMirrorStatus(link, 'could not fetch timestamp due to missing "Access-Control-Allow-Origin" header');
      } else if (this.status == 404) {
        // old dump without timestamp file
        setMirrorStatus(link, 'outdated');
      } else {
        console.log('checkMirrorStatus() url: ' + url + ', status: ' + this.status + ', response: ' + this.responseText);
        setMirrorStatus(link, 'unable to determine');
      }
    }
  };

  xhr.send();
}

$(document).ready(function() {
  $(".mirrorstatus").each(function() {
    console.log('ready() enhance mirror status');
    // extract url from sibling
    var url = this.previousSibling.href;
    // add link to query mirror status
    $(this).empty();
    $(this).append('&nbsp;<a class="badge" href="#" onclick="javascript:checkMirrorStatus(this, \'' + url + '\'); return false;">query mirror status</a>');
  });
});

function checkAllMirrors() {
  $(".mirrorstatus a.badge").each(function() {
    // extract url from parent sibling
    var url = this.parentNode.previousSibling.href;
    checkMirrorStatus(this, url);
  });
}
