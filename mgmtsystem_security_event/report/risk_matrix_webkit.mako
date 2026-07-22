## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
.matrix_wrapper {
  border: 1px solid black;
}

.severity_label {
  min-height: 120px;
  width: 30px;
  margin-left: 40px;
  margin-right: -30px;
  margin-top: 35px;
  margin-bottom: -35px;
  -webkit-transform: rotate(-90deg);
}
        </style>
    </head>
    <body>
        <%setLang(user.lang)%>

        %for matrix in objects:
        <table>
          <tr>
            <td style="font-size: 18px; font-weight: bold">${_('Risk Matrix')}</td>
          </tr>
          <tr>
            <td style="margin-bottom: 30px; font-size: 14px;">${matrix.get_type()}</td>
          </tr>
        </table>

        <table class="matrix_wrapper">
          <tr>
            <td style="-webkit-transform: rotate(-90deg); padding-top:${len(matrix.get_severities()) * 100 / 2}px: margin-left: -60px; width: 30px; font-weight: bold">
              ${_('Severity')}
            </td>
            <td>
              <table class="risk_matrix">
                %for s in matrix.get_severities():
                <tr>
                  <td>
                    <div class="severity_label">
                      ${matrix.severity_name(s)}
                    </div>
                  </td>
                  </td>
                  %for p in matrix.get_probabilities():
                  <td style="background-color:${matrix.get_cell_color(s, p)}; font-size: 12px;">
                    %for e in matrix.get_event_list(s, p):
                      ${e.name}<br/>
                    %endfor
                  </td>
                  %endfor
                </tr>
                %endfor

                <tr>
                  <td></td>
                  %for p in matrix.get_probabilities():
                  <td style="padding-right:20px;">${matrix.probability_name(p)}</td>
                  %endfor
                </tr>
                <tr>
                  <td></td>
                  <td colspan="${len(matrix.get_probabilities())}" style="text-align:center; height: 50px; font-weight: bold">
                    ${_('Probability')}
                  </td>
                </tr>
              </table>
            %endfor
            </td>
          </tr>
        </table>
      </div>
    </body>
</html>
