package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.tsinghua.thss.popcorn.config.Config;

public class RecordListActivity extends Activity {

    ProgressDialog progressDialog;
    private String[] mBrief, mFormContent, mFormId;
    private TableListAdapter mAdapter;
    private String mRouteId;
    private static int REQUEST_CODE = 2, ONE_SUBMIT_FINISHED = 3;
    private ListView myListView;
    private Button submitBtn;
    private int completedForm;
    private int oneSubmitMessage = 0;
    SharedPreferences sp;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record_list);

        Bundle tmp_bundle = this.getIntent().getExtras();
        mRouteId = tmp_bundle.getString("route_id");
        sp = getApplicationContext().getSharedPreferences("recordData", MODE_PRIVATE);

        mAdapter = new TableListAdapter(this);
        submitBtn = (Button) findViewById(R.id.recordlist_submit);

        submitBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                completedForm = sp.getInt("route_" + mRouteId, 0);
                if (completedForm < mBrief.length) {
                    new AlertDialog.Builder(RecordListActivity.this)
                            .setTitle("路线上的抄表并未全部完成，是否确定提交？")
                            .setNegativeButton("确定", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    sendRouteFormData();
                                }
                            })
                            .setPositiveButton("取消", null)
                            .show();
                } else {
                    sendRouteFormData();
                }
            }
        });

        myListView = (ListView) findViewById(R.id.recordlist_listview);
        myListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> adapter, View view, int position,
                                    long id) {
                Intent intent = new Intent(RecordListActivity.this, TableActivity.class);
                Bundle bundle = new Bundle();
                bundle.putString("brief", mBrief[(int) id]);
                bundle.putString("form_content", mFormContent[(int) id]);
                bundle.putString("id", mFormId[(int) id]);
                bundle.putString("route_id", mRouteId);
                intent.putExtras(bundle);
                startActivityForResult(intent, REQUEST_CODE);
            }

        });

        getFormList();
    }

    private void getFormList(){
        RequestParams params = new RequestParams();
        params.addQueryStringParameter("route_id", mRouteId);
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.FORM_GET_URL,
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
                            ArrayList<String> tmp_title = new ArrayList<String>();
                            ArrayList<String> tmp_form_content = new ArrayList<String>();
                            ArrayList<String> tmp_id = new ArrayList<String>();
                            if (status.equals("ok")) {
                                JSONArray results = jsonObject.getJSONArray("data");
                                for (int i = 0; i < results.length(); ++i) {
                                    JSONObject result = results.getJSONObject(i);
                                    String name = result.getString("name");
                                    String form_content = result.getString("content");
                                    String id = result.getString("id");
                                    tmp_title.add(name);
                                    tmp_form_content.add(form_content);
                                    tmp_id.add(id);
                                }
                                mBrief = tmp_title.toArray(new String[]{});
                                mFormContent = tmp_form_content.toArray(new String[]{});
                                mFormId = tmp_id.toArray(new String[]{});
                                myListView.setAdapter(mAdapter);
                                submitBtn.setVisibility(View.VISIBLE);
                            } else {
                                Toast.makeText(getApplicationContext(), "该路线未设置设备", Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }

                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getApplicationContext(), "网络故障", Toast.LENGTH_SHORT).show();
                    }
                });
    }

    private void sendRouteFormData(){
        progressDialog = new ProgressDialog(RecordListActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);// 设置水平进度条
        progressDialog.setCanceledOnTouchOutside(false);// 设置在点击Dialog外是否取消Dialog进度条
        progressDialog.setCancelable(false);
        progressDialog.setIndeterminate(false);
        progressDialog.setMax(100);
        progressDialog.setMessage("数据提交中...");
        progressDialog.show();

        final int completed = completedForm;
        oneSubmitMessage = 0;

        for(int i = 0; i < mBrief.length; i++) {
            String cacheFormData = sp.getString("route_" + mRouteId + "_form_" + mFormId[i], "");
            if(cacheFormData.equals("")) continue;
            RequestParams params = new RequestParams();
            params.addBodyParameter("username", Config.DEBUG_USERNAME);
            params.addBodyParameter("access_token", Config.ACCESS_TOKEN);
            params.addBodyParameter("route_id", mRouteId);
            params.addBodyParameter("brief", mBrief[i]);
            params.addBodyParameter("content", cacheFormData);

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

                            try {
                                JSONObject jsonObject = new JSONObject(responseInfo.result);
                                String status = jsonObject.getString("status");
                                if (status.equals("ok")) {
                                    SharedPreferences.Editor editor = sp.edit();
                                    int remain = sp.getInt("route_" + mRouteId, 0);
                                    if(remain != 0) {
                                        editor.putInt("route_" + mRouteId, remain - 1);
                                        editor.apply();
                                        remain -= 1;
                                        progressDialog.setProgress(100 * (completed - remain) / completed);
                                    }
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            sendOneSubmitFinishedMessage();
                        }

                        @Override
                        public void onFailure(HttpException error, String msg) {
                            sendOneSubmitFinishedMessage();
                        }
                    });
        }
    }

    private  void sendOneSubmitFinishedMessage(){
        Message message = new Message();
        message.what = ONE_SUBMIT_FINISHED;
        handler.sendMessage(message);
    }

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            if (msg.what == ONE_SUBMIT_FINISHED) {
                oneSubmitMessage += 1;
                if(oneSubmitMessage == completedForm){
                    int remain = sp.getInt("route_" + mRouteId, -1);
                    if(remain == 0) {
                        SharedPreferences.Editor editor = sp.edit();
                        for(int i = 0; i < mBrief.length; i++) {
                            editor.remove("route_" + mRouteId + "_form_" + mFormId[i]);
                            editor.apply();
                        }
                        progressDialog.dismiss();
                        myListView.setAdapter(mAdapter);
                        new AlertDialog.Builder(RecordListActivity.this)
                                .setTitle("提交数据成功！")
                                .setPositiveButton("确定", null)
                                .show();
                    } else {
                        progressDialog.dismiss();
                        new AlertDialog.Builder(RecordListActivity.this)
                                .setTitle("网络故障，请重新提交！")
                                .setPositiveButton("确定", null)
                                .show();
                    }
                }
            }
            super.handleMessage(msg);
        };
    };

    class ViewHolder {
        public TextView title;
        public FontAwesomeText faText;
    }

    public class TableListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public TableListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mBrief.length;
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText(mBrief[position]);

            SharedPreferences sp = getApplicationContext().getSharedPreferences("recordData", MODE_PRIVATE);
            if(!sp.getString("route_" + mRouteId +"_form_" + mFormId[position], "").equals("")) {
                holder.faText.setTextColor(Color.parseColor("#D3D3D3"));
            }
           return convertView;
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (Activity.RESULT_OK == resultCode && requestCode == REQUEST_CODE) {
            myListView.setAdapter(mAdapter);
            //mAdapter.notifyDataSetChanged();
        }
    }

    @Override
    public void finish() {
        RecordListActivity.this.setResult(RESULT_OK, null);
        super.finish();
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.record, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RecordListActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}