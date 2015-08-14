package cn.edu.tsinghua.thss.popcorn.formgenerator;

import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.TextView;

import cn.edu.tsinghua.thss.popcorn.MainActivity;
import cn.edu.tsinghua.thss.popcorn.R;

public class FormNumericEditText extends FormWidget
{
	protected TextView _label;
	protected EditText _input;
	protected int _priority;
	protected Drawable originalDrawable;
		
	public FormNumericEditText(Context context, String property ) 
	{
		super( context, property );
		
		_label = new TextView( context );
		_label.setText( getDisplayText() );
		
		_input = new EditText( context );
		_input.setInputType( InputType.TYPE_CLASS_PHONE );
		_input.setLayoutParams(FormActivity.defaultLayoutParams);

		originalDrawable = _input.getBackground();
		
		_layout.addView( _label );
		_layout.addView( _input );
	}

	public String getValue() {
		return _input.getText().toString();
	}

	public void setValue(String value) {
		_input.setText(value);
	}

	public static boolean isNumeric(String str){
		if (str.length() == 0){
			return false;
		}
		for (int i = str.length();--i>=0;){
			if (!Character.isDigit(str.charAt(i))){
				return false;
			}
		}
		return true;
	}

	public boolean isNumber(String number){
		int index = number.indexOf(".");
		if(index<0){
			return isNumeric(number);
		}else{
			String num1 = number.substring(0,index);
			String num2 = number.substring(index+1);
			return isNumeric(num1) && isNumeric(num2);
		}
	}

	@Override
	public void setThresholdChecker(final String maxStr, final String minStr) {
		_input.addTextChangedListener(
				new TextWatcher() {
					@Override
					public void onTextChanged(CharSequence s, int start, int before,
											  int count) {

					}

					@Override
					public void beforeTextChanged(CharSequence s, int start, int count,
												  int after) {

					}

					@Override
					public void afterTextChanged(Editable s) {
						if(isNumber(s.toString())) {
							Double textValue = Double.valueOf(s.toString());
							Double max = Double.MAX_VALUE, min = Double.MIN_VALUE;
							if (isNumeric(maxStr)) {
								max = Double.valueOf(maxStr);
							}
							if (isNumeric(minStr)) {
								min = Double.valueOf(minStr);
							}
							if (textValue >= min && textValue <= max) {
								int sdk = android.os.Build.VERSION.SDK_INT;
								if(sdk < android.os.Build.VERSION_CODES.JELLY_BEAN) {
									_input.setBackgroundDrawable(originalDrawable);
								} else {
									_input.setBackground(originalDrawable);
								}
							} else {
								_input.setBackgroundResource(R.drawable.edittext_background_warning);
							}
						}else{
							_input.setBackgroundResource(R.drawable.edittext_background_warning);
						}
					}
				}
		);
	}
	
	@Override 
	public void setHint( String value ){
		_input.setHint( value );
	}
}
