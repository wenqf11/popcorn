package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;

import cn.edu.tsinghua.thss.popcorn.QRcode.CheckinActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.formgenerator.FormActivity;

public class TableActivity extends FormActivity{
    static private int REQUEST_CODE = 2;
    private String  result;
    private String mRouteId;
    private String mFormId;
    private String mBrief;
    private TextView resultTextView;

    private void saveButtonClick(JSONObject json) {
        Toast.makeText(getApplicationContext(), "暂存成功", Toast.LENGTH_SHORT).show();
        SharedPreferences sp = getApplicationContext().getSharedPreferences("recordData", MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();

        if(sp.getString("route_" + mRouteId+"_form_" + mFormId, "").equals("")){
            int numOfForms = sp.getInt("route_" + mRouteId, 0);
            editor.putInt("route_" + mRouteId, numOfForms + 1);
        }
        editor.putString("route_" + mRouteId+"_form_" + mFormId, json.toString());
        editor.apply();

        TableActivity.this.finish();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Bundle tmp_bundle = this.getIntent().getExtras();
        String form_content_json = tmp_bundle.getString("form_content");
        mBrief = tmp_bundle.getString("brief");
        mRouteId = tmp_bundle.getString("route_id");
        mFormId = tmp_bundle.getString("id");

        if (form_content_json.length() < 10) {
            form_content_json = "{\"未添加抄表表单\":{\"id\":\"1\",\"type\":\"integer\",\"hint\":\"未添加抄表表单\"}}";
        }

        SharedPreferences sp = getApplicationContext().getSharedPreferences("recordData", MODE_PRIVATE);
        String cacheFormData = sp.getString("route_" + mRouteId + "_form_" + mFormId, "");

        JSONObject cacheObj = null;
        if(!cacheFormData.equals("")) {
            try {
                JSONObject schema = new JSONObject(form_content_json);
                cacheObj = new JSONObject(cacheFormData);
                JSONObject property;
                JSONArray names = schema.names();
                String name;
                for (int i = 0; i < names.length(); i++) {
                    name = names.getString(i);
                    property = schema.getJSONObject(name);
                    property.put("value", cacheObj.getString(name));
                }
                form_content_json = schema.toString();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        LinearLayout container = generateForm( form_content_json );

        final ScrollView sc = (ScrollView)container.getChildAt(0);
        LinearLayout layoutInSc = (LinearLayout)sc.getChildAt(sc.getChildCount()-1);
        LinearLayout list = new LinearLayout(this);
        list.setGravity(Gravity.RIGHT);
        Button btn = new Button(this);
        resultTextView = new TextView(this);
        resultTextView.setGravity(Gravity.CENTER);
        try {
            if (cacheObj.getString("qrcode").length() > 0){
                resultTextView.setText(cacheObj.getString("qrcode"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        btn.setText("签到");
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(TableActivity.this, CheckinActivity.class);
                Bundle bundle = new Bundle();
                intent.putExtras(bundle);
                startActivityForResult(intent, REQUEST_CODE);
            }
        });

        list.addView(resultTextView);
        list.addView(btn);

        //container.addView(list);
        layoutInSc.addView(list);

        Button submitBtn = new Button(this);
        submitBtn.setText("暂存");
        submitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JSONObject json = save();
                String qrcode = (String) resultTextView.getText();
                if (qrcode.length() > 0) {
                    try {
                        json.put("qrcode", qrcode);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

                boolean isEmpty = false;
                try {
                    Iterator<?> it = json.keys();
                    String key = "";
                    String value = "";
                    while (it.hasNext()) {
                        key = it.next().toString();
                        value = json.getString(key);
                        if (value.length() < 1) {
                            isEmpty = true;
                        }
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                if (isEmpty) {
                    new AlertDialog.Builder(TableActivity.this)
                            .setTitle("所有项都是必填的，不能为空！")
                            .setPositiveButton("确定", null)
                            .show();
                    return;
                }

                saveButtonClick(json);
            }
        });
        layoutInSc.addView(submitBtn);

        container.setPadding(20, 20, 20, 20);
        setContentView(container);
    }

        @Override
    public void finish() {
        TableActivity.this.setResult(RESULT_OK, null);
        super.finish();
    }

    /**
    * 处理回传值
    * 第二窗体返回值，在此方法中进行处理。
    */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // super.onActivityResult(requestCode, resultCode, data);
        //比对之前的请求编码，以及核对活动返回的编码是否是Activity.RESULT_OK
        if (Activity.RESULT_OK == resultCode && requestCode == REQUEST_CODE) {
            result = data.getStringExtra("device_brief");
            resultTextView.setText(result);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.table, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            TableActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
