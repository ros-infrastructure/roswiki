// version.js, based on SeeSaw 1.0
function Version(sections) {
  var dotversion = ".version.";

  // Tag shows unless already tagged
  $.each(sections.show, function() {
    $("span.version." + this).not(".versionshow,.versionhide").filter(".hidepart").addClass("versionshow").end().filter(".showpart").addClass("versionhide");
  });
  $.each(sections.show, function() {
    $("div" + dotversion + this).not(".versionshow,.versionhide").addClass("versionshow");
  });

  // Tag hides unless already tagged
  $.each(sections.hide, function() {
    $("span.version." + this).not(".versionshow,.versionhide").filter(".showpart").addClass("versionshow").end().filter(".hidepart").addClass("versionhide");
  });
  $.each(sections.hide, function() {
    $("div" + dotversion + this).not(".versionshow,.versionhide").addClass("versionhide");
  });

  // Show or hide according to tag
  $(".versionshow").removeClass("versionshow").filter("span").show().end().filter("div").show();
  $(".versionhide").removeClass("versionhide").filter("span").hide().end().filter("div").hide();

  if (sections.show[0]) {
    var name = sections.show[0];
    var capitalized_name = name.charAt(0).toUpperCase() + name.slice(1);
    $(".rosversion_name").text(name);
    $(".rosversion_name_cap").text(capitalized_name);
  }
}

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

function toggleDocStatus()
{
  if ($("#doc_status").is(":hidden")) {
    $("#doc_status").slideDown();
  } else {
    $("#doc_status").slideUp();
  }
}

$(document).ready(function() {
  var activedistro = "indigo"; //CHANGE THIS LINE TO CHANGE THE DISTRO DISPLAYED BY DEFAULT
  var url_distro = getURLParameter('distro');
  if (url_distro) {
    activedistro=url_distro;
  }
  // Make the %ROSDISTRO%/%rosdistro% syntax work by wrapping them in spans. This is
  // necessary vs. MoinMoin macros because macros are not expanded in code blocks.
  var original = $("#page").html();
  var replaced = original.
    replace(/%ROSDISTRO%/g,'<span class="rosversion_name_cap">%ROSDISTRO%</span>').
    replace(/%rosdistro%/g,'<span class="rosversion_name">%rosdistro%</span>');
  if (original != replaced) {
    $("#page").html(replaced);
  }
  $("div.version").hide();
  if ($("#"+activedistro).length > 0) {
    $("#"+activedistro).click();
  } else {
    $("#rosversion_selector button:last").click();
  }
  $("input.version:hidden").each(function() {
    var bg = $(this).attr("value").split(":");
    $("div.version." + bg[0]).css("background-color",bg[1]).removeClass(bg[0]);
  });
});
