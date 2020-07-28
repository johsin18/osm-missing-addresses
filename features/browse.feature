Feature: show and add primitives in the browser and in external editors

  Scenario: open toolbox on a match
    Given summary is loaded
    When user opened toolbox for Identical Street 1
    Then toolbox opens for Identical Street 1

  Scenario: click "show in openstreetmap.org" on a match
    Given summary is loaded
    When user opened toolbox for Identical Street 1
    When user clicked Show in openstreetmap.org
    Then new tab showing OSM way with ID 1 will open

  Scenario: click "show in openstreetmap.org" on a missing address
    Given summary is loaded
    When user opened toolbox for Missing Street 2
    When user clicked Show in openstreetmap.org
    Then new tab showing OSM at location 2.10000/2.20000

  Scenario: click "show in openstreetmap.org" on a surplus address
    Given summary is loaded
    When user opened toolbox for Surplus Street 4
    When user clicked Show in openstreetmap.org
    Then new tab showing OSM node with ID 31 will open
