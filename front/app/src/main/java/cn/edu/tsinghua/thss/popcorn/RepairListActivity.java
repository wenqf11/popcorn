package cn.edu.tsinghua.thss.popcorn;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

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

public class RepairListActivity extends ListActivity {
    private List<Map<String, Object>> mData;
    JSONArray repairTaskList = null;
    ProgressDialog progressDialog;

    Handler handler = new Handler() {
        public void handleMessage(Message msg) {
            getRepairTaskList();
            super.handleMessage(msg);
        };
    };
    Timer timer = new Timer();
    TimerTask task = new TimerTask() {

        @Override
        public void run() {
            // 需要做的事:发送消息
            Message message = new Message();
            message.what = 1;
            handler.sendMessage(message);
        }
    };

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        progressDialog = new ProgressDialog(RepairListActivity.this, R.style.buffer_dialog);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.setMessage("数据加载中...");
        progressDialog.setIndeterminate(false);
        progressDialog.setCancelable(false);
        progressDialog.show();
        //getRepairTaskList();
        timer.schedule(task, Config.REPAIR_UPDATE_DELAY, Config.REPAIR_UPDATE_INTERVAL); // 1s后执行task,经过2s再次执行
        progressDialog.hide();
    }

    private void getRepairTaskList(){

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.REPAIR_TASK_LIST_URL,
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
                                repairTaskList = jsonObject.getJSONArray("data");
                                mData = getData();
                                DeviceListAdapter adapter = new DeviceListAdapter (RepairListActivity.this);
                                setListAdapter(adapter);
                            }
                            else{
                                Toast.makeText(getApplicationContext(), "服务器内部出错", Toast.LENGTH_SHORT).show();
                            }
                        }catch (JSONException e){
                            e.printStackTrace();
                        }
                        //progressDialog.hide();
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        //progressDialog.hide();
                        Toast.makeText(getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent = new Intent(this, RepairActivity.class);
        Bundle bundle = new Bundle();
        JSONObject task = null;
        try {
            task = repairTaskList.getJSONObject(position);
            bundle.putString("task", task.toString());
            intent.putExtras(bundle);
            startActivity(intent);
        } catch (Exception e) {
        }

        super.onListItemClick(l, v, position, id);
    }


    private List<Map<String, Object>> getData() {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        if (repairTaskList != null) {
            for (int i = 0; i < repairTaskList.length(); i++) {
                Map<String, Object> map = new HashMap<String, Object>();
                try {
                    JSONObject tempObject = repairTaskList.getJSONObject(i);
                    map.put("title", tempObject.getString("title"));
                    map.put("confirmed", tempObject.getString("confirmed"));
                    list.add(map);
                } catch (Exception e) {
                }
            }
        }
        return list;
    }

    class ViewHolder {
        public TextView title;
        public FontAwesomeText faText;
    }

    public class DeviceListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public DeviceListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mData.size();
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
                convertView = mInflater.inflate(R.layout.listview_repair, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText((String)mData.get(position).get("title"));
            if(position == 1) {
                holder.faText.setTextColor(Color.parseColor("#D3D3D3"));
            }
            return convertView;
        }
    }


    @Override
    protected  void onDestroy(){
        progressDialog.dismiss();
        super.onDestroy();
        timer.cancel();
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
            RepairListActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

}