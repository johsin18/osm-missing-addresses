Feature: customize view, i.e. hide/show matches, missing, surplus

  Scenario: hide
    Given summary is loaded
    When user toggles matches
    Then matches are hidden

  Scenario: hide and show matches
    Given summary is loaded
    When user toggles matches
    When user toggles matches
    Then matches are shown

  Scenario: hide
    Given summary is loaded
    When user toggles missing
    Then missing are hidden

  Scenario: hide and show matches
    Given summary is loaded
    When user toggles missing
    When user toggles missing
    Then missing are shown

  Scenario: hide
    Given summary is loaded
    When user toggles surplus
    Then surplus are hidden

  Scenario: hide and show matches
    Given summary is loaded
    When user toggles surplus
    When user toggles surplus
    Then surplus are shown
