package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.NoRepeatToast;
import cn.edu.tsinghua.thss.popcorn.utils.SharedPreferencesUtil;

public class ChangeLocalSettingActivity extends Activity {
    Spinner spinner;

    @OnClick(R.id.submit_settings_btn)
    private void submitSettingsButtonClick(View v) {
        try {
            int pos = spinner.getSelectedItemPosition();
            SharedPreferencesUtil.putInt(ChangeLocalSettingActivity.this, Config.VIBRATE_DURATION, pos);
        } catch (Exception e)
        {
            Toast.makeText(getApplicationContext(), "设置保存失败！", Toast.LENGTH_SHORT).show();
            return ;
        }
        Toast.makeText(getApplicationContext(), "设置保存成功！", Toast.LENGTH_SHORT).show();
        ChangeLocalSettingActivity.this.finish();
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_local_setting);

        spinner = (Spinner) findViewById(R.id.vibrate_duration);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.vibrate_duration,
                R.layout.my_spinner_textview);
        adapter.setDropDownViewResource(R.layout.my_spinner_textview);
        spinner.setAdapter(adapter);
        int pos = SharedPreferencesUtil.getInt(ChangeLocalSettingActivity.this, Config.VIBRATE_DURATION, 0);
        spinner.setSelection(pos);
        ViewUtils.inject(this);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.feedback, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            ChangeLocalSettingActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
