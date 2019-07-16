# from flask_wtf import FlaskForm
# from wtforms import StringField, validators, SelectField, SubmitField

# class EmbedSearch(FlaskForm):
#     embedcode = StringField('embedcode', validators=[validators.InputRequired(),validators.length(max=200),validators.Optional(strip_whitespace=True)])
#     ad_id = StringField('Adset ID', validators=[ validators.length(max=200),validators.Optional(strip_whitespace=True)])
#     playerType = SelectField('Select Player', choices=[('1', 'BasicPlayer Activity'), ('2', 'OoyalaPlayer with Skin only non-OTP/DRM'), ('3', 'Test OPT/DRM asset with events'), ('4', 'ChromeCast App - Coming soon'), ('5', 'IMA Preconfigured'), ('6', 'Chrome (Player v4)'), ('7', 'Webview (Player v4)')])
#     syndicationOverride = SelectField('Syndication Override', choices=[('1', ' False'), ('2', 'True')])
#     autoPlay = SelectField('Auto Play', choices=[('1', ' False'), ('2', 'True')])
#     entitlementID = StringField('Account ID',validators=[validators.length(max=100)])
#     chromecastAppID = StringField('Chromecast App ID',validators=[validators.length(max=100)])
#     v4Params = StringField('Player v4 params',validators=[validators.length(max=300)])
#     vast_tag = StringField('VAST tag URL (Shortened)',validators=[validators.length(max=50)])
#     debug_page = StringField('Debug Page (Shortened)',validators=[validators.length(max=50)])
#     search_embed = SubmitField(label='Search')
#     appNotification = SubmitField(label='Genarate QR Code')`
