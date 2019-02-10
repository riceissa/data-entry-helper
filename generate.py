#!/usr/bin/env python3

import re

DLW_DOCUMENTS_FIELDS = [
        ("URL", "url", "varchar", 200),
        ("Title", "title", "varchar", 200),
        ("Publication date", "publication_date", "date", None),
        ("Modified date", "modified_date", "date", None),
        ("Author", "author", "varchar", 200),
        ("Publisher", "publisher", "varchar", 200),
        ("Affected donors", "affected_donors", "varchar", 200),
        ("Affected donees", "affected_donees", "varchar", 200),
        ("Document scope", "document_scope", "enum", ['Launch','Pre-launch planning','Broad donor strategy','Single donation documentation','Donee periodic update','Donee donation case','Evaluator review of donee','Evaluator update on donee','Evaluator consolidated recommendation list','Periodic donation list documentation','Reasoning supplement','Third-party coverage of donor strategy','Third-party case for donation','Third-party case against donation','Donation suggestion list', 'Unsolicited third-party suggestions for donor','Review of current state of cause area', 'Status change','Miscellaneous commentary', 'Donee AMA', 'Evaluator retrospective','Evaluator quantification approach','Job advertisement','Request for proposals','Request for reviews of donee']),
        ("Cause area", "cause_area", "varchar", 200),
        ("Notes", "notes", "varchar", 2000),
        ]


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

FIELDS = DLW_DOCUMENTS_FIELDS

def parse_line(line):
    sql_column = ""
    sql_type = ""
    sql_type_params = None
    m = re.match(r"""\s+([A-Za-z_]+)\s+([A-Za-z]+)\(([^)]+)\)""", line)
    if m:
        sql_column = m.group(1)
        sql_type = m.group(2)
        sql_type_params = m.group(3)
    # I might want to do some shotgun parsing like in https://github.com/riceissa/fred-processing/blob/master/modify_sql.py
    if sql_type == "enum":
        m = re.match(r""" """, sql_type_params)
    return (sql_column, sql_type, sql_type_params)


def main():
    print(r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <script>
    function clearForm() {
        document.getElementsByName("myForm")[0].reset();
    }

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
             <input type="button" onclick="clearForm()" value="Clear form">
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
    elif sql_type == "int" or sql_type == "float":
        result += """<input type="text" name="{}"><br />""".format(sql_column)
    elif sql_type == "date":
        result += """<input type="text" name="{}"><br />""".format(sql_column)
    elif sql_type == "varchar":
        if sql_type_params <= 200:
            result += """<input type="text" size="80" name="{}"><br />""".format(sql_column)
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
