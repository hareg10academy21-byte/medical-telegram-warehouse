  - name: fct_messages
    description: "Fact table containing Telegram messages."
    columns:
      - name: message_id
        tests:
          - unique
          - not_null

      - name: channel_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_channels')
              field: channel_key

      - name: date_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_dates')
              field: date_key

      - name: views
        tests:
          - not_null