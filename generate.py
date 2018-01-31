#!/usr/bin/env python3

FIELDS = [
        ("Donations data update regularity",
         "donations_data_update_regularity",
         "enum",
         ['continuous updates', 'monthly refresh', 'quarterly refresh',
          'annual refresh', 'irregular']),
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
        result += """<select id="{}">""".format(sql_column)
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
    return result


def script_part(first, label, sql_column, sql_type, sql_type_params=None):
    result = """sql += {}sqlQuote(f("{}"));""".format('' if first else '"," + ',
                                                    sql_column)
    return result


if __name__ == "__main__":
    main()
