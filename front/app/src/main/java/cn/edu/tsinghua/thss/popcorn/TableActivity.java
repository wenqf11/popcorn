package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;

import cn.edu.tsinghua.thss.popcorn.QRcode.QRcodeActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.formgenerator.FormActivity;

public class TableActivity extends FormActivity{
    static private int REQUEST_CODE = 2;
    private String  result;
    private String mRouteId;
    private String mBrief;
    private TextView resultTextView;
    private ProgressDialog progressDialog;

    private void submitButtonClick(JSONObject json) {
        String id = "";
        try{
            //id = maintainTask.getString("id");
        }catch (Exception e){
        }
        //String note = maintainResultEditText.getText().toString();

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("route_id", mRouteId);
        params.addBodyParameter("brief", mBrief);
        params.addBodyParameter("content", json.toString());

        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String time = df.format(new Date());
        params.addBodyParameter("timestamp", time);

        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.POST,
                Config.SUBMIT_METER_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {

                        try{
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");
                            if(status.equals("ok")) {
                                Toast.makeText(getApplicationContext(), "提交成功", Toast.LENGTH_SHORT).show();
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "提交失败，请重新提交", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }

    private String wrap_form_content(String raw) {
        String form_content_json = raw;
        return form_content_json;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Bundle tmp_bundle = this.getIntent().getExtras();
        String form_content_raw = tmp_bundle.getString("form_content");
        mBrief = tmp_bundle.getString("brief");
        mRouteId = tmp_bundle.getString("route_id");
        String form_content_json = wrap_form_content(form_content_raw);

        progressDialog = new ProgressDialog(TableActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("抄表数据提交中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);

        //LinearLayout container = generateForm( FormActivity.parseFileToString( this, "schemas.json" ) );
        if (form_content_json.length() < 10) {
            form_content_json = "{\"未添加抄表表单\":{\"id\":\"1\",\"type\":\"integer\",\"hint\":\"未添加抄表表单\"}}";
        }
        LinearLayout container = generateForm( form_content_json );

        LinearLayout list = new LinearLayout(this);
        list.setGravity(Gravity.RIGHT);
        Button btn = new Button(this);
        resultTextView = new TextView(this);
        resultTextView.setGravity(Gravity.CENTER);
        btn.setText("签到");
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(TableActivity.this, QRcodeActivity.class);
                Bundle bundle = new Bundle();
                intent.putExtras(bundle);
                startActivityForResult(intent, REQUEST_CODE);
            }
        });

        list.addView(resultTextView);
        list.addView(btn);
        container.addView(list);



        Button submitBtn = new Button(this);
        submitBtn.setText("提交");
        submitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                JSONObject json = save();
                String qrcode = (String)resultTextView.getText();
                if (qrcode.length() > 0) {
                    //json.put("qrcode", qrcode);
                }
                submitButtonClick(json);
            }
        });
        container.addView(submitBtn);

        container.setPadding(20,20,20,20);
        setContentView(container);
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
            result = data.getStringExtra("result");
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
