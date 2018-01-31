#!/usr/bin/env python3

FIELDS = [
        ("Donor", "donor", "varchar", 100),
        ("Donor type", "donor_type", "enum", ['Individual','Couple','Donor group','Subsidiary','Private foundation']),
        ("Country", "country", "varchar", 40),
        ("Facebook username", "facebook_username", "varchar", 100),
        ("Website", "website", "varchar", 100),
        ("Donations URL", "donations_url", "varchar", 1000),
        ("LW username", "lesswrong_username", "varchar", 40),
        ("LinkedIn username", "linkedin_username", "varchar", 100),
        ("Affiliated orgs (All current and former employers, plus orgs they are board members or advisors for, but restricting to orgs that are either potential donees or other nonprofits with significant footprint in the associated communities)", "affiliated_orgs", "varchar", 1000),
        ("EA Forum username", "eaf_username", "varchar", 40),
        ("EA Hub username", "eahub_username", "varchar", 40),
        ("GitHub username", "github_username", "varchar", 40),
        ("Twitter username", "twitter_username", "varchar", 40),
        ("PredictionBook username", "predictionbook_username", "varchar", 40),
        ("Philosophy URL (URL to grant/giving philosophy)", "philosophy_url", "varchar", 200),
        ("Grant application process URL", "grant_application_process_url", "varchar", 200),
        ("Donations data update regularity",
         "donations_data_update_regularity",
         "enum",
         ['continuous updates', 'monthly refresh', 'quarterly refresh',
          'annual refresh', 'irregular']),
        ("Donations data DLW update regularity", "donations_data_dlw_update_regularity", "enum", ['continuous updates','monthly refresh','quarterly refresh','annual refresh','irregular']),
        ("Donations data update lag", "donations_data_update_lag", "enum", ['none','days','months','years']),
        ("Donations data DLW update lag", "donations_data_dlw_update_lag", "enum", ['none','days','months','years']),
        ("DLW data processing script", "dlw_data_processing_script", "varchar", 100),
        ("Wikipedia page (URL)", "wikipedia_page", "varchar", 120),
        ("Best overview URL", "best_overview_url", "varchar", 200),
        ("Brief history", "brief_history", "varchar", 2000),
        ("Brief donor focus notes", "brief_donor_focus_notes", "varchar", 2000),
        ("Grant decision logistics notes", "grant_decision_logistics_notes", "varchar", 2000),
        ("Grant publication logistics notes", "grant_publication_logistics_notes", "varchar", 2000),
        ("Grant financing notes", "grant_financing_notes", "varchar", 2000),
        ("Notes", "notes", "varchar", 5000),
        ]

def main():
    print(r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <script>
    var firstTime = true;

    function f(x) {
      return document.forms["myForm"][x].value;
    }

    function sqlQuote(x) {
      if (! x) {
        return "NULL";
      }
      x = x.replace(/\\/g, "\\\\");
      x = x.replace(/'/g, "''");
      x = x.replace(/\n/g, "\\n");
      return "'" + x + "'";
    }

    function sqlNumber(x) {
      if (! x) {
        return "NULL";
      }
      return x;
    }
    function checkForm() {
      var sql = "(";""")

    first = True
    for field in FIELDS:
        print(script_part(first, *field))
        first = False

    print(r"""sql += ")";

      // prompt("Name", sql);

      if (firstTime) {
        document.getElementById("formOutput").innerHTML =
          sql + "\n";
        firstTime = false;
      } else {
        document.getElementById("formOutput").innerHTML +=
          "," + sql + "\n";
      }
      return false;
    }
  </script>
</head>""")

    print("""<body>

  <p>Enter data in the form below and submit to produce a SQL insert tuple.</p>

  <form name="myForm" onsubmit="return checkForm()" method="get">""")

    for field in FIELDS:
        print(form_part(*field))

    print("""<input type="submit" value="Submit">
             </form>""")
    print("""<p>
  <pre><code><textarea rows="30" cols="100" id="formOutput">Output will appear here</textarea></code></pre>
  </p>
            </body>""")


    print("""</html>""")


def form_part(label, sql_column, sql_type, sql_type_params=None):
    result = label + ": "
    if sql_type == "enum":
        result += """<select id="{}">
                        <option value="">NULL</option>""".format(sql_column)
        for option in sql_type_params:
            result += "<option>" + option + "</option>"
        result += "</select><br />"
    elif sql_type == "int":
        result += """<input type="text" name="{}"><br />""".format(sql_column)
    elif sql_type == "date":
        result += """<input type="text" name="{}"><br />""".format(sql_column)
    elif sql_type == "varchar":
        if sql_type_params <= 200:
            result += """<input type="text" name="{}"><br />""".format(sql_column)
        else:
            result += """<br />
                <textarea rows="5" cols="80" id="{}"></textarea>
                <br />""".format(sql_column)
    else:
        raise ValueError("We don't know this SQL type.")
    return result


def script_part(first, label, sql_column, sql_type, sql_type_params=None):
    result = """sql += {}sqlQuote(f("{}"));""".format('' if first else '"," + ',
                                                    sql_column)
    return result


if __name__ == "__main__":
    main()
