Feature: clicking "Recompute" triggers recompute of the address diff

  Scenario: click "Recompute" while everything is okay
    Given summary is loaded
    When user clicked Recompute
    Then page will show a late datetime as Generation time
