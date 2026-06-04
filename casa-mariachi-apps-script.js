// ============================================================
// Casa Mariachi - Google Apps Script
// Paste this into script.google.com, deploy as Web App
// ============================================================

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();

    // Add header row if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Phone Number', 'Submitted At', 'Source', 'Date Added']);
    }

    var phone = e.parameter.phone || '';
    var ts    = e.parameter.ts    || '';
    var src   = e.parameter.source || 'casa-mariachi-page';

    sheet.appendRow([phone, ts, src, new Date()]);

    return ContentService
      .createTextOutput(JSON.stringify({status:'ok'}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch(err) {
    return ContentService
      .createTextOutput(JSON.stringify({status:'error', msg: err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test by running this in the script editor
function test() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow(['(720) 555 0100', new Date().toISOString(), 'manual-test', new Date()]);
  Logger.log('Test row added');
}
