Feature: Getting a collection
  Scenario: Collection does not exist
    Given namespace life does exist
    When we GET "/v1/namespaces/life/collections/happiness"
    Then the response code will be 404
    And the response will contain
      """
        {
          "errors": [{
            "code": "C404",
            "status": "404",
            "title": "Collection not found",
            "detail": "Collection \"happiness\" was not found in namespace \"life\""
          }]
        }
      """

  Scenario Outline: Insuffcient permissions to namespace
    Given namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have <permission> permissions to collection additional-pylons
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 403
    And the response will contain
      """
        {
          "errors": [{
            "code": "403",
            "status": "403",
            "title": "Forbidden",
            "detail": "READ permission or higher is required to perform this action"
          }]
        }
        """

    Examples: Permissions
      | permission |
      | CREATE     |
      | UPDATE     |
      | DELETE     |

  Scenario Outline: Namespace permissions trickle
    Given namespace construct exists
    And we have <permission> permissions to namespace construct
    And collection additional-pylons exists in namespace construct
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200

    Examples: Permissions
      | permission |
      | ADMIN      |
      | READ       |
      | CRUD       |
      | READ_WRITE |

  Scenario: Collection return value
    Given the time is 2015-01-01T00:00:00.0000Z
    And namespace construct exists
    And collection additional-pylons exists in namespace construct
    And we have READ permissions to collection additional-pylons
    When we GET "/v1/namespaces/construct/collections/additional-pylons"
    Then the response code will be 200
    And the response will contain
      """
      {
        "data": {
            "id": "additional-pylons",
            "type": "collections",
            "attributes": {
              "name": "additional-pylons",
              "permissions": {
                "user-testing-we": 2,
                "user-testing-system": 9223372036854775807
              }
            },
            "meta": {
              "created-by": "user-testing-system",
              "modified-by": "user-testing-system",
              "created-on": "2015-01-01T00:00:00",
              "modified-on": "2015-01-01T00:00:00"
            },
            "relationships": {
              "documents": {
                "links": {
                  "self": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents",
                  "related": "http://localhost:50325/v1/namespaces/construct/collections/additional-pylons/documents"
                }
              }
            }
          }
      }
      """
