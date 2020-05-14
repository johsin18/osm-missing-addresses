function getPageCoordinates(element) {
  let box = element.getBoundingClientRect();

  return {
    left: box.left + pageXOffset,
    top: box.top + pageYOffset
  };
}

let selectedAddress = null;

let mainTable = document.getElementById("mainTable")
let toolWindow = document.getElementById('toolWindow');
let linkShowInOsmOrg = document.getElementById('linkShowInOsmOrg');
let linkLoadInJosm = document.getElementById('linkLoadInJosm');
let linkAddInJosm = document.getElementById('linkAddInJosm');
let linkRequestIgnore = document.getElementById('linkRequestIgnore');
let customReasonButton = document.getElementById('customReasonButton');
let customReasonInput = document.getElementById('customReasonInput');
let primitiveReference = null;
let primitiveType = null;
let primitiveId = null;
let streetName = null;
let housenumber = null;
let exists = null;

function closeToolbox() {
  toolWindow.style.display = 'none';
  if (selectedAddress != null) {  // formerly selected address
    selectedAddress.removeAttribute('selected');
  }
  selectedAddress = null;
}

mainTable.addEventListener('click', e => {
  let clickedElement = document.elementFromPoint(e.clientX, e.clientY);
  if (selectedAddress != null) {  // formerly selected address
    selectedAddress.removeAttribute('selected');
  }
  if (clickedElement instanceof AddressMatch || clickedElement instanceof AddressMissing || clickedElement instanceof AddressSurplus) {
    selectedAddress = clickedElement;
    selectedAddress.setAttribute('selected', '');

    let box = getPageCoordinates(selectedAddress);
    toolWindow.style.left = (box.left - 40) + 'px';
    toolWindow.style.top = (box.top + 20) + 'px';
    toolWindow.style.display = 'block';
    if (selectedAddress instanceof AddressMatch || selectedAddress instanceof AddressSurplus) {
      primitiveReference = selectedAddress.getAttribute('p');
      primitiveType = primitiveReference.substring(0, 1);
      switch(primitiveType) {
        case "n":
          primitiveType = "node";
          break;
        case "w":
          primitiveType = "way";
          break;
        case "r":
          primitiveType = "relation";
          break;
      }
      primitiveId = primitiveReference.substring(1);

      linkLoadInJosm.removeAttribute("disabled")
    } else {
      linkLoadInJosm.setAttribute("disabled", "")
    }

    if (selectedAddress instanceof AddressMatch || selectedAddress instanceof AddressSurplus) {
      linkShowInOsmOrg.href = "https://www.openstreetmap.org/" + primitiveType + "/" + primitiveId;
    } else  {
      const [lat, lon] = getCoordinates();
      linkShowInOsmOrg.href = "https://www.openstreetmap.org/#map=19/" + lat + "/" + lon + "&layers=N";
    }

    let streetNameElement = selectedAddress.parentElement/*table cell*/.parentElement/*table row*/.firstChild/*white space text*/.nextSibling/*street name cell*/;
    streetName = streetNameElement.textContent;
    housenumber = selectedAddress.textContent;
    exists = (selectedAddress instanceof AddressSurplus);

    selectIgnoreReason();

  } else {
    closeToolbox();
  }
});

function getCoordinates() {
  let coordinates = selectedAddress.getAttribute('c').split(",");
  return [parseFloat(coordinates[0]), lon = parseFloat(coordinates[1])];
}

function showInJosm() {
  if (selectedAddress == null)
    return;
  const [lat, lon] = getCoordinates();
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:8111/load_and_zoom?left=" + (lon - 0.0006) + "&right=" + (lon + 0.0006) + "&top=" + (lat + 0.0004) + "&bottom=" + (lat - 0.0004));
  request.send();
}

function loadPrimitiveInJosm() {
  if (selectedAddress == null)
    return;
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:8111/load_object?objects=" + primitiveReference + "&relation_members=true");
  request.send();
}

function addLatLonInJosm() {
  const [lat, lon] = getCoordinates();
  let request = new XMLHttpRequest();
  let query = "http://localhost:8111/add_node?lat=" + lat + "&lon=" + lon + "&addtags=addr:street=" + streetName + "|addr:housenumber=" + housenumber;
  request.open("GET", encodeURI(query));
  request.send();
}

function requestIgnore(clickedReasonButton) {
  let reason = null;
  if (clickedReasonButton == customReasonButton) {
    reason = customReasonInput.value;
  } else {
    reason = clickedReasonButton.textContent;
  }
  exists = !(selectedAddress instanceof AddressMissing);
  let request = new XMLHttpRequest();
  request.open("PUT", "./addresses_to_ignore?street=" + streetName + "&housenumber=" + housenumber + "&exists=" + exists + "&reason=" + reason);
  request.send();

  selectedAddress.setAttribute('ignored', '');
  selectedAddress.setAttribute('reason', reason);
  selectIgnoreReason(reason);
}

function selectIgnoreReason() {
  reason = selectedAddress.getAttribute('reason');
  let reasonButtons = toolWindow.querySelectorAll("button");
  let found = false;
  reasonButtons.forEach(button =>
    { if(button.textContent == reason) {
        button.setAttribute('selected', '');
        found =true;
      } else {
        button.removeAttribute('selected');
      }
    });
  if (!found) {
    if (reason != null) {
      customReasonInput.value = reason;
      customReasonButton.setAttribute('selected', '');
    }
  }
}

// Keep the tag names as short as possible, to keep document size minimal

class AddressMatch extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
    this.classList.add("address");
  }
}
customElements.define('a-i', AddressMatch);  // "a-i" == address identical

class AddressMissing extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
    this.classList.add("address");
  }
}
customElements.define('a-m', AddressMissing);

class AddressSurplus extends HTMLElement {
  constructor() {
    // Always call super first in constructor
    super();
    this.classList.add("address");
  }
}
customElements.define('a-s', AddressSurplus);

document.getElementById('matches').checked = true;
document.getElementById('missing').checked = true;
document.getElementById('surplus').checked = true;

columnSwitches = {}
function toggleColumn(toggleCheckbox) {
  columnClass = toggleCheckbox.id;
  if (!toggleCheckbox.checked) {
    let sheet = document.createElement('style');
    sheet.innerHTML = "td." + columnClass + ",th." + columnClass + " { display: none; } ";
    document.body.appendChild(sheet);
    columnSwitches[columnClass] = sheet;
  } else if (columnSwitches[columnClass] != null) {
    let sheet = columnSwitches[columnClass];
    sheet.parentElement.removeChild(sheet);
  }
}

function triggerRecompute() {
  let request = new XMLHttpRequest();
  request.open("POST", "./recompute_summary");
  request.send();
}
