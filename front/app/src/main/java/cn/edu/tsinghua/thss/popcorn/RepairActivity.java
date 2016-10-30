package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
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

import java.util.Calendar;

import cn.edu.tsinghua.thss.popcorn.config.Config;


public class RepairActivity extends Activity {
    private int position = -1;
    private boolean isConfirmed = false;
    private boolean isUpdated = false;
    private boolean isSubmitted = false;
    private String updatedNote = "";

    private JSONObject repairTask = null;
    ProgressDialog progressDialog;

    @ViewInject(R.id.repair_report_title)
    private TextView reportTitleTextView;

    @ViewInject(R.id.repair_device_number)
    private TextView deviceNumberTextView;

    @ViewInject(R.id.repair_reporter)
    private TextView reporterTextView;

    @ViewInject(R.id.repair_report_datetime)
    private TextView reportDatetimeTextView;

    @ViewInject(R.id.repair_fault_description)
    private TextView faultDescriptionTextView;

    @ViewInject(R.id.repair_memo)
    private TextView repairMemoTextView;

    @ViewInject(R.id.repair_result)
    private TextView repairResultEditText;

    @ViewInject(R.id.repair_update)
    private Button repairUpdateButton;

    @OnClick(R.id.repair_update)
    private void updateRepairButtonClick(View v){
        String id = "";
        try{
            id = repairTask.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }
        String note = repairResultEditText.getText().toString();
        updatedNote = note;


        if(note.length() <  2){
            Toast.makeText(getApplicationContext(), "维修结论太短，暂存失败！", Toast.LENGTH_SHORT).show();
        }else {
            RequestParams params = new RequestParams();
            params.addBodyParameter("username", Config.DEBUG_USERNAME);
            params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
            params.addBodyParameter("maintain_id", id);
            params.addBodyParameter("note", note);
            progressDialog.show();


            HttpUtils http = new HttpUtils();
            http.send(HttpRequest.HttpMethod.POST,
                    Config.REPAIR_TASK_UPDATE_URL,
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

                            try {
                                JSONObject jsonObject = new JSONObject(responseInfo.result);
                                String status = jsonObject.getString("status");
                                if (status.equals("ok")) {
                                    Toast.makeText(getApplicationContext(), "暂存成功", Toast.LENGTH_SHORT).show();
                                    isUpdated = true;
                                } else {
                                    Toast.makeText(getApplicationContext(), "暂存失败，请重新提交", Toast.LENGTH_SHORT).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            progressDialog.hide();
                        }


                        @Override
                        public void onFailure(HttpException error, String msg) {
                            Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                            progressDialog.hide();
                        }
                    });
        }
    }

    @ViewInject(R.id.repair_submit)
    private Button repairSubmitButton;

    @OnClick(R.id.repair_submit)
    private void submitRepairButtonClick(View v) {
        if (repairSubmitButton.getText().equals("提交")) {
            if(repairResultEditText.getText().toString().length() <  2){
                Toast.makeText(getApplicationContext(), "维修结论太短，提交失败！", Toast.LENGTH_SHORT).show();
            }else {
                new AlertDialog.Builder(RepairActivity.this)
                        .setTitle("提示")
                        .setMessage("提交后内容将无法修改，是否确定提交？")
                        .setNegativeButton("确定",
                                new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialoginterface, int i) {
                                        submitData();
                                    }
                                }).setPositiveButton("取消", null).show();
            }
        }else{
            acceptTask();
        }
    }

    private void acceptTask(){
        String id = "";
        try{
            id = repairTask.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("maintain_id", id);
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.REPAIR_TASK_CONFIRM_URL,
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
                                Toast.makeText(getApplicationContext(), "成功接受维修任务", Toast.LENGTH_SHORT).show();
                                repairSubmitButton.setText("提交");
                                repairUpdateButton.setVisibility(View.VISIBLE);
                                isConfirmed = true;
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "接受任务失败，请重新提交", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }

    private void submitData(){
        String id = "";
        try{
            id = repairTask.getString("id");
        }catch (Exception e){
            e.printStackTrace();
        }
        String note = repairResultEditText.getText().toString();

        RequestParams params = new RequestParams();
        params.addBodyParameter("username", Config.DEBUG_USERNAME);
        params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
        params.addBodyParameter("maintain_id", id);
        params.addBodyParameter("note", note);
        progressDialog.show();

        HttpUtils http = new HttpUtils();
        http.send(HttpRequest.HttpMethod.POST,
                Config.REPAIR_TASK_SUBMIT_URL,
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
                                isSubmitted = true;
                                RepairActivity.this.finish();
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
                        Toast.makeText(getApplicationContext(), "网络连接异常，请检查网络连接！", Toast.LENGTH_SHORT).show();
                        progressDialog.hide();
                    }
                });
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_repair);


        Bundle bundle = this.getIntent().getExtras();
        try {
            repairTask = new JSONObject(bundle.getString("task"));
            position = bundle.getInt("position");
        }catch (Exception e) {
        }
        progressDialog = new ProgressDialog(RepairActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);

        ViewUtils.inject(this);
        setValueOfTextView();
    }

    private void setValueOfTextView(){
        String title = "";
        String deviceNumber = "";
        String faultDescription = "";
        String repairMemo = "";
        String repairResult = "";
        String creator = "";
        String create_time = "";
        String confirmed = "";
        try{
            title = repairTask.getString("title");
            deviceNumber = repairTask.getString("device_brief");
            faultDescription = repairTask.getString("description");
            creator = repairTask.getString("creator");
            create_time = repairTask.getString("create_time");
            repairMemo = repairTask.getString("memo");
            repairResult = repairTask.getString("note");
            confirmed = repairTask.getString("confirmed");
        }catch (Exception e){
            e.printStackTrace();
        }

        int index = repairMemo.indexOf("审核未通过：");
        if (index < 0){
            index = 0;
        }
        repairMemo = repairMemo.substring(index);

        reportTitleTextView.setText(title);
        reporterTextView.setText(creator);
        reportDatetimeTextView.setText(create_time);
        deviceNumberTextView.setText(deviceNumber);
        faultDescriptionTextView.setText(faultDescription);
        repairMemoTextView.setText(repairMemo);
        repairResultEditText.setText(repairResult);
        if(confirmed.equals("true")) {
            repairSubmitButton.setText("提交");
            repairUpdateButton.setVisibility(View.VISIBLE);
        }else{
            repairSubmitButton.setText("接受任务");
        }
    }

    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
    }

    @Override
    public void finish() {
        Bundle bundle = new Bundle();
        bundle.putInt("position", position);
        bundle.putBoolean("isConfirmed", isConfirmed);
        bundle.putBoolean("isUpdated", isUpdated);
        bundle.putBoolean("isSubmitted", isSubmitted);
        bundle.putString("updatedNote", updatedNote);
        RepairActivity.this.setResult(RESULT_OK, RepairActivity.this.getIntent().putExtras(bundle));

        super.finish();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.repair, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RepairActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
